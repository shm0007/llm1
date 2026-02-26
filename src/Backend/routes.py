from flask import Blueprint, request, jsonify
from openai_api import get_openai_embedding, summarize_text, test_openai_api_key
from bert import get_bert_embedding,get_gpt_oss_embedding,get_baai_embedding,get_e5_embedding,get_labse_embedding
from bert import get_ft_scibert_embedding,get_ft_bert_embedding,get_ft_roberta_embedding,get_ft_secbert_embedding,get_ft_securebert_embedding,get_bert_embedding, get_scibert_embedding,get_roberta_embedding,get_securebert_embedding,get_secbert_embedding

from weaviate_class import WeaviateClass
import os

from huggingface_hub import login

hf_token = os.getenv("HF_TOKEN")
if hf_token:
    login(token=hf_token)
else:
    raise RuntimeError("HF_TOKEN not found. Make sure it is set in .env file.")

# Initialize the blueprint
routes = Blueprint('routes', __name__)

# Intialize Weaviate client
weaviateDB = WeaviateClass()

from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import re
# ============================
# GPU-only LLM Loader (Swap Cache)
# Supports:
#   - GPT-OSS (bf16)
#   - Llama 4 (NVIDIA FP8 checkpoints)  ✅ your chosen option
# ============================

import gc
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

# ---- Pick the model IDs you want ----
MODEL_REGISTRY = {
    "GPT-OSS": "openai/gpt-oss-20b",
    "LLAMA3.1": "meta-llama/Llama-3.1-8B-Instruct",
    "llama4-maverick": "meta-llama/Llama-4-Maverick-17B-128E-Instruct",
}

# ---- Single-model cache (prevents OOM by keeping only one model loaded) ----
_CURRENT_ENGINE = None
_tokenizer = None
_model = None


def _unload_current_model():
    """Free GPU memory of the currently loaded model."""
    global _tokenizer, _model

    _tokenizer = None
    if _model is not None:
        try:
            _model.to("cpu")
        except Exception:
            pass
    _model = None

    gc.collect()
    if torch.cuda.is_available():
        torch.cuda.empty_cache()


def get_llm(engine: str):
    print(f"Requested LLM engine: {engine}",flush=True)
    """
    Load one engine on GPU and keep it cached.
    Switching engines unloads the previous one to avoid GPU OOM.
    """
    global _CURRENT_ENGINE, _tokenizer, _model

    if engine not in MODEL_REGISTRY:
        raise ValueError(f"Unknown engine '{engine}'. Options: {list(MODEL_REGISTRY.keys())}")

    if _CURRENT_ENGINE == engine and _tokenizer is not None and _model is not None:
        return _tokenizer, _model

    # Swap: unload old model, load new model
    _unload_current_model()

    model_id = MODEL_REGISTRY[engine]

    _tokenizer = AutoTokenizer.from_pretrained(model_id)
    _model = AutoModelForCausalLM.from_pretrained(
        model_id,
        device_map="auto",          # GPU-only
        torch_dtype=torch.bfloat16, # good default; FP8 models handle FP8 internally
    )
    
    _model.eval()

    _CURRENT_ENGINE = engine
    return _tokenizer, _model
def clear_cuda_memory():
    gc.collect()                      # Free Python objects
    if torch.cuda.is_available():
        torch.cuda.empty_cache()      # Release unused cached memory
        torch.cuda.ipc_collect() 
def build_prompt(text: str) -> str:
    return f"""<|begin_of_text|>
<|start_header_id|>system<|end_header_id|>
You are a careful assistant that summarizes text accurately.
<|eot_id|>
<|start_header_id|>user<|end_header_id|>
Summarize the following text clearly and concisely.

TEXT:
{text}
<|eot_id|>
<|start_header_id|>assistant<|end_header_id|>
""".strip()

def summarizeLLLAMA(text: str, engine: str, max_new_tokens: int = 250) -> str:
    clear_cuda_memory()
    tok, mdl = get_llm(engine)
    prompt = build_prompt(text)
    print("LLAMA Prompt:",flush=True)
    inputs = tok(prompt, return_tensors="pt")
    input_ids = inputs["input_ids"].to(mdl.device)
    attention_mask = inputs["attention_mask"].to(mdl.device)

    with torch.no_grad():
        output_ids = mdl.generate(
            input_ids=input_ids,
            attention_mask=attention_mask,
            max_new_tokens=max_new_tokens,
            temperature=0.2,
            top_p=0.95,
            repetition_penalty=1.1,
            do_sample=True,
            eos_token_id=tok.eos_token_id,
        )

    new_tokens = output_ids[0, input_ids.shape[-1]:]
    summary = tok.decode(new_tokens, skip_special_tokens=True).strip()
    print(f"LLAMA Summary:||{summary}||",flush=True)
    return summary
def summarize_with_engine(engine: str, query: str, text: str, max_new_tokens: int = 2048) -> str:
    """
    Generate a cybersecurity-focused explanation/summary using the selected engine.
    engine options:
      - "gpt-oss"
      - "llama4-scout-fp8"
      - "llama4-maverick-fp8"
    """

    # if engine.startswith("LLAMA"):
    #     return summarizeLLLAMA(text,engine=engine, max_new_tokens=max_new_tokens)
    clear_cuda_memory()
    tok, mdl = get_llm(engine)
    print("Generating summary with engine:", engine,flush=True)
    messages = [

        {"role": "user", "content": f"""
You are interacting with a cybersecurity analysis system that maps user-provided text descriptions or queries to relevant Common Weakness Enumerations (CWEs) and MITRE ATT&CK techniques.
 
The user has provided the following query or description:
---------------------------------------------
{query}
---------------------------------------------
 
Based on this input, the system has identified the following relevant CWEs and ATT&CK patterns:
---------------------------------------------
{text}
---------------------------------------------
 
Using the identified CWEs and ATT&CK patterns listed above, generate a response that addresses the user’s query or description. Remove any CWE or ATT&CK patterns that are not relevant to the user query. The response should explain the security implications, potential risks, and relevant attack behaviors reflected by these mappings. 
"""
         },
    ]

    inputs = tok.apply_chat_template(
        messages,
        add_generation_prompt=True,   # important for instruct/chat models
        return_tensors="pt",
        return_dict=True,
    ).to(mdl.device)

    banned_phrases = ["analysis", "we need", "Summary", "Here is", "We will", "Let's"]
    bad_words_ids = tok(banned_phrases, add_special_tokens=False).input_ids

    with torch.no_grad():
        out = mdl.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            do_sample=True,
            temperature=0.6,
            top_p=0.9,
            repetition_penalty=1.15,
            no_repeat_ngram_size=4,
            eos_token_id=tok.eos_token_id,
            pad_token_id=tok.eos_token_id,
            bad_words_ids=bad_words_ids,
        )

    gen_tokens = out[0][inputs["input_ids"].shape[-1]:]
    return tok.decode(gen_tokens, skip_special_tokens=True).strip()





# bert combined search endpoint
@routes.route('/search', methods=['POST'])
def search_combined_bert():
    summarizerEngine = request.args.get("summarizer", "None").strip()
    modelName = request.args.get("model", "BERT").strip()
    print(summarizerEngine,flush=True)
    print(modelName,flush=True)
    schema = weaviateDB.client.schema.get()
    print('---------------Weaviate Schema Classes:---------------',flush=True)
    print([c["class"] for c in schema.get("classes", [])],flush=True)
    if modelName == "BERT":
        weaviateDB.wipe_all_data()
        weaviateDB.store_bert()
        weaviateDB.weaviateModelStatus = "BERT"
    elif modelName == "BAAI":
        weaviateDB.wipe_all_data()
        weaviateDB.store_baai()
        weaviateDB.weaviateModelStatus = "BAAI"
    elif modelName == "GPT-OSS":
        _unload_current_model()
        weaviateDB.wipe_all_data()
        weaviateDB.store_gpt_oss()
        weaviateDB.weaviateModelStatus = "GPTOSS"
    elif modelName == "E5":
        weaviateDB.wipe_all_data()
        weaviateDB.store_e5()
        weaviateDB.weaviateModelStatus = "E5"
    elif modelName == "LaBSE":
        weaviateDB.wipe_all_data()
        weaviateDB.store_labse()
        weaviateDB.weaviateModelStatus = "LaBSE"
            
    data = request.json
    query_text = data.get('query', '')
    if modelName == "BERT":
        # Generate BERT embedding for the query
        query_embedding = get_bert_embedding(query_text)
    elif modelName == "GPT-OSS":
        # Generate GPT-OSS embedding for the query
        query_embedding = get_gpt_oss_embedding(query_text)
        print("GPT-OSS Embedding Generated",flush=True)
    elif modelName == "BAAI":
        # Generate BAAI embedding for the query
        query_embedding = get_baai_embedding(query_text)
        print("BAAI Embedding Generated",flush=True)
    elif modelName == "E5":
        # Generate E5 embedding for the query
        query_embedding = get_e5_embedding(query_text)
        print("E5 Embedding Generated",flush=True)
    elif modelName == "LaBSE":
        # Generate LaBSE embedding for the query
        query_embedding = get_labse_embedding(query_text)
        print("LaBSE Embedding Generated",flush=True)
    print(f"Query Embedding Generated {len(query_embedding)}",flush=True)
    # Perform semantic search on CWE data
    cwe_results = (

        weaviateDB.cwe_bert_query(query_embedding)
    )

    # Perform semantic search on Attack data
    attack_results = (
        weaviateDB.attack_bert_query(query_embedding)
    )

    # Format results for CWE
    cwe_formatted_results = [
        {
            "CWE ID": result.get("cweID", "N/A"),
            "Name": result.get("name", "N/A"),
            "Description": result.get("description", "No description available"),
            "Similarity": 1 - float(result.get("_additional","Additional").get('distance',"Distance N/A")),
            "Extended Description": result.get("extendedDescription", "No extended description available")
        }
        for result in cwe_results.get("data", {}).get("Get", {}).get("CWE_Entry", [])
    ]

    # Format results for Attack
    attack_formatted_results = [
        {
            "Attack ID": result.get("attackID", "N/A"),
            "Type": result.get("type", "N/A"),
            "Name": result.get("name", "N/A"),
            "Similarity": 1 - float(result.get("_additional","Additional").get('distance',"Distance N/A")),
            "Description": result.get("description", "No description available")
        }
        for result in attack_results.get("data", {}).get("Get", {}).get("Attack_Entry", [])
    ]
    # print("CWE Formatter Results-------------------",flush=True)
    # print(cwe_formatted_results,flush=True)
    # if summarizerEngine == "None":
    #     summary_cwe = cwe_formatted_results
    #     summary_attack = attack_formatted_results
    # else:
    #     summary_cwe = summarize_with_engine(summarizerEngine, str(query_text), str(cwe_formatted_results)+str(attack_formatted_results))
    #     summary_attack = ""#summarize_with_engine(summarizerEngine, str(query_text), str(attack_formatted_results))

    # print("CWE Summaray Results-------------------",flush=True)
    # print(summary_attack,flush=True)
    # print("Attack Summaray Results-------------------",flush=True)
    # print(summary_attack,flush=True)
    

    payload = {
    "CWE Results": cwe_formatted_results,
    "Attack Results": attack_formatted_results}

    print(payload, flush=True)          # ✅ prints actual data
    return jsonify(payload)


# bert combined search endpoint
@routes.route('/summary', methods=['POST'])
def summarize_gpt_oss_llama():
    summarizerEngine = request.args.get("summarizer", "None").strip()
    print(summarizerEngine,flush=True)
            
    data = request.json
    query_text = data.get('query', '')
    cwe_formatted_results = data.get('message', '')




    if summarizerEngine == "None":
        summary_cwe = cwe_formatted_results
    else:
        summary_cwe = summarize_with_engine(summarizerEngine, str(query_text), str(cwe_formatted_results))
    
    print(jsonify({
        "Summary": summary_cwe,
    }),flush=True)
   
    payload = {
        "Summary": summary_cwe,
    }

    print(payload, flush=True)          # ✅ prints actual data
    return jsonify(payload)


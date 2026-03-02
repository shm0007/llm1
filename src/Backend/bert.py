import gc
from transformers import AutoModelForCausalLM, BertTokenizer, BertModel

from transformers import AutoTokenizer, AutoModel
import torch
# Function to generate BERT embeddings
def get_bert_embedding(text):
    # Initialize BERT tokenizer and model
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    model = BertModel.from_pretrained('bert-base-uncased')
    
    inputs = tokenizer(text, return_tensors='pt', truncation=True, max_length=512, padding=True)
    outputs = model(**inputs)
    return outputs.last_hidden_state.mean(dim=1).squeeze().detach().numpy()
# Optional: cache so you don't reload the model every call
_GPT_OSS_ID = "openai/gpt-oss-20b"
_gpt_tokenizer = None
_gpt_model = None

def _get_gpt_oss():
    global _gpt_tokenizer, _gpt_model
    if _gpt_tokenizer is None or _gpt_model is None:
        _gpt_tokenizer = AutoTokenizer.from_pretrained(_GPT_OSS_ID)

        # Ensure pad token exists (needed for padding=True)
        if _gpt_tokenizer.pad_token is None:
            _gpt_tokenizer.pad_token = _gpt_tokenizer.eos_token

        dtype = torch.bfloat16 if torch.cuda.is_available() else torch.float32
        _gpt_model = AutoModelForCausalLM.from_pretrained(
            
            _GPT_OSS_ID,
            device_map="auto",   # use GPU if available
            torch_dtype=dtype,
        )
        _gpt_model.eval()
    return _gpt_tokenizer, _gpt_model


def get_gpt_oss_embedding(text):
    """
    Returns: np.ndarray of shape (hidden_dim,)
    Matches the roberta function's output style (numpy vector).
    """

    gc.collect()
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
    print("Generating GPT-OSS embedding...",flush=True)
    tokenizer, model = _get_gpt_oss()
    device = next(model.parameters()).device

    inputs = tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        max_length=512,
        padding=True,
    )
    inputs = {k: v.to(device) for k, v in inputs.items()}

    with torch.no_grad():
        outputs = model(**inputs, output_hidden_states=True, return_dict=True)
        last_hidden = outputs.hidden_states[-1]  # (1, T, H)

        # Masked mean pooling (ignore padding)
        mask = inputs["attention_mask"].unsqueeze(-1).to(last_hidden.dtype)  # (1, T, 1)
        summed = (last_hidden * mask).sum(dim=1)                             # (1, H)
        denom = mask.sum(dim=1).clamp(min=1e-9)                              # (1, 1)
        emb = (summed / denom).squeeze(0)                                    # (H,)
    del model
    del tokenizer
    del inputs
    del outputs
    del last_hidden
    del mask

    gc.collect()
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
    return emb.float().cpu().numpy()
def get_roberta_embedding(text):
    # Initialize BERT tokenizer and model
    tokenizer = AutoTokenizer.from_pretrained('roberta-base')
    model = AutoModel.from_pretrained('roberta-base')
    
    inputs = tokenizer(text, return_tensors='pt', truncation=True, max_length=512, padding=True)
    outputs = model(**inputs)
    return outputs.last_hidden_state.mean(dim=1).squeeze().detach().numpy()
def get_e5_embedding(text):
    tokenizer = AutoTokenizer.from_pretrained("intfloat/e5-base-v2")
    model = AutoModel.from_pretrained("intfloat/e5-base-v2")

    text = f"passage: {text}"

    inputs = tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        max_length=512,
        padding=True,
    )
    outputs = model(**inputs)

    return outputs.last_hidden_state.mean(dim=1).squeeze().detach().numpy()
def get_labse_embedding(text):
    tokenizer = AutoTokenizer.from_pretrained("setu4993/LaBSE")
    model = AutoModel.from_pretrained("setu4993/LaBSE")

    text = f"passage: {text}"

    inputs = tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        max_length=512,
        padding=True,
    )
    outputs = model(**inputs)

    return outputs.last_hidden_state.mean(dim=1).squeeze().detach().numpy()

def get_baai_embedding(text):
    # Initialize BERT tokenizer and model
    tokenizer = AutoTokenizer.from_pretrained('BAAI/bge-large-en-v1.5')
    model = AutoModel.from_pretrained('BAAI/bge-large-en-v1.5')

    inputs = tokenizer(text, return_tensors='pt', truncation=True, max_length=512, padding=True)
    outputs = model(**inputs)
    return outputs.last_hidden_state.mean(dim=1).squeeze().detach().numpy()
    


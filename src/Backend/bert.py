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
    
def get_securebert_embedding(text):
    # Initialize BERT tokenizer and model
    tokenizer = AutoTokenizer.from_pretrained('ehsanaghaei/SecureBERT')
    model = AutoModel.from_pretrained('ehsanaghaei/SecureBERT')
    
    inputs = tokenizer(text, return_tensors='pt', truncation=True, max_length=512, padding=True)
    outputs = model(**inputs)
    return outputs.last_hidden_state.mean(dim=1).squeeze().detach().numpy()
def get_v2_securebert_embedding(text):
    # Initialize BERT tokenizer and model
    tokenizer = AutoTokenizer.from_pretrained('cisco-ai/SecureBERT2.0-base')
    model = AutoModel.from_pretrained('cisco-ai/SecureBERT2.0-base')
    
    inputs = tokenizer(text, return_tensors='pt', truncation=True, max_length=512, padding=True)
    outputs = model(**inputs)
    return outputs.last_hidden_state.mean(dim=1).squeeze().detach().numpy()

def get_secbert_embedding(text):
    # Initialize BERT tokenizer and model
    tokenizer = AutoTokenizer.from_pretrained('jackaduma/SecBERT')
    model = AutoModel.from_pretrained('jackaduma/SecBERT')
    
    inputs = tokenizer(text, return_tensors='pt', truncation=True, max_length=512, padding=True)
    outputs = model(**inputs)
    return outputs.last_hidden_state.mean(dim=1).squeeze().detach().numpy()

def get_ft_scibert_embedding(text):
    # Initialize BERT tokenizer and model
    tokenizer = AutoTokenizer.from_pretrained('ehsan0007/scibert_cwe_attack')
    model = AutoModel.from_pretrained('ehsan0007/scibert_cwe_attack')
    
    inputs = tokenizer(text, return_tensors='pt', truncation=True, max_length=512, padding=True)
    outputs = model(**inputs)
    return outputs.last_hidden_state.mean(dim=1).squeeze().detach().numpy()
def get_ft_secbert_embedding(text):
    # Initialize BERT tokenizer and model
    tokenizer = AutoTokenizer.from_pretrained('ehsan0007/secbert_cwe_attack')
    model = AutoModel.from_pretrained('ehsan0007/secbert_cwe_attack')
    
    inputs = tokenizer(text, return_tensors='pt', truncation=True, max_length=512, padding=True)
    outputs = model(**inputs)
    return outputs.last_hidden_state.mean(dim=1).squeeze().detach().numpy()
def get_ft_securebert_embedding(text):
    # Initialize BERT tokenizer and model
    tokenizer = AutoTokenizer.from_pretrained('ehsan0007/securebert_cwe_attack')
    model = AutoModel.from_pretrained('ehsan0007/securebert_cwe_attack')
    
    inputs = tokenizer(text, return_tensors='pt', truncation=True, max_length=512, padding=True)
    outputs = model(**inputs)
    return outputs.last_hidden_state.mean(dim=1).squeeze().detach().numpy()
def get_ft_bert_embedding(text):
    # Initialize BERT tokenizer and model
    tokenizer = AutoTokenizer.from_pretrained('ehsan0007/bert_cwe_attack')
    model = AutoModel.from_pretrained('ehsan0007/bert_cwe_attack')
    
    inputs = tokenizer(text, return_tensors='pt', truncation=True, max_length=512, padding=True)
    outputs = model(**inputs)
    return outputs.last_hidden_state.mean(dim=1).squeeze().detach().numpy()
def get_ft_roberta_embedding(text):
    # Initialize BERT tokenizer and model
    tokenizer = AutoTokenizer.from_pretrained('ehsan0007/roberta_cwe_attack')
    model = AutoModel.from_pretrained('ehsan0007/roberta_cwe_attack')
    
    inputs = tokenizer(text, return_tensors='pt', truncation=True, max_length=512, padding=True)
    outputs = model(**inputs)
    return outputs.last_hidden_state.mean(dim=1).squeeze().detach().numpy()





# Load once (faster than reloading inside the function)
_SCIBERT_ID = "allenai/scibert_scivocab_uncased"
_scibert_tok = AutoTokenizer.from_pretrained(_SCIBERT_ID)
_scibert_mdl = AutoModel.from_pretrained(_SCIBERT_ID)
_scibert_mdl.eval()

@torch.no_grad()
def get_scibert_embedding(text: str):
    """
    Returns a SciBERT embedding for `text` using mean pooling over token embeddings.
    Shape: (hidden_size,) as a NumPy array.
    """
    inputs = _scibert_tok(text, return_tensors="pt", truncation=True, max_length=512, padding=True)
    outputs = _scibert_mdl(**inputs)                       # last_hidden_state: [B, L, H]
    last = outputs.last_hidden_state
    mask = inputs["attention_mask"].unsqueeze(-1)          # [B, L, 1]
    emb = (last * mask).sum(dim=1) / mask.sum(dim=1)       # mean-pool, [B, H]
    return emb.squeeze(0).cpu().numpy()


# If you prefer CLS pooling instead of mean-pooling:
# def get_scibert_embedding(text: str):
#     inputs = _scibert_tok(text, return_tensors="pt", truncation=True, max_length=512, padding=True)
#     outputs = _scibert_mdl(**inputs)
#     cls = outputs.last_hidden_state[:, 0, :]              # [CLS] token
#     return cls.squeeze(0).cpu().numpy()

import json
import os

#cwe_data_file_bert = 'vectorized_cwe_data.txt'
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

cwe_data_file_bert = os.path.join(BASE_DIR, "vectorized_cwe_data.txt")
cwe_data_file_bert = os.path.join(BASE_DIR, "vectorized_cwe_data.txt")
cwe_data_file_baai = os.path.join(BASE_DIR, "cwe_baai_embeddings.txt")
cwe_data_file_e5 = os.path.join(BASE_DIR, "cwe_e5_embeddings.txt")
cwe_data_file_labse = os.path.join(BASE_DIR, "cwe_labse_embeddings.txt")

cwe_data_file_sci_bert = os.path.join(BASE_DIR, "cwe_sci_bert_embeddings.txt")
cwe_data_file_ft_sci_bert = os.path.join(BASE_DIR, "cwe_ft_sci_bert_embeddings.txt")
cwe_data_file_ft_sec_bert = os.path.join(BASE_DIR, "cwe_ft_sec_bert_embeddings.txt")
cwe_data_file_ft_bert = os.path.join(BASE_DIR, "cwe_ft_bert_embeddings.txt")
cwe_data_file_ft_roberta = os.path.join(BASE_DIR, "cwe_ft_sec_roberta_embeddings.txt")

cwe_data_file_ft_secure_bert = os.path.join(BASE_DIR, "cwe_ft_secure_bert_embeddings.txt")

cwe_data_file_securebert = os.path.join(BASE_DIR, "cwe_secure_bert_embeddings.txt")
cwe_data_file_v2securebert = os.path.join(BASE_DIR, "cwe_v2_securebert_embeddings.txt")
cwe_data_file_secbert = os.path.join(BASE_DIR, "cwe_sec_bert_embeddings.txt")

cwe_data_file_roberta = os.path.join(BASE_DIR, "cwe_roberta_embeddings.txt")
cwe_data_file_gpt_oss = os.path.join(BASE_DIR, "cwe_gpt_oss_embeddings.txt")


#cwe_data_file_openai = 'openapi_cwe_embeddings.json'
cwe_data_file_openai = os.path.join(BASE_DIR, "openapi_cwe_embeddings.json")


# Load and parse the CWE data file
def  load_cwe_data_gpt_oss():
    cwe_data = []
    embeddings = []
    with open(cwe_data_file_gpt_oss, 'r', encoding='utf-8') as f:
        entry = {}
        embedding = []
        for line in f:
            line = line.strip()
            if line.startswith("CWE ID:"):
                entry["cweID"] = line.split("CWE ID:", 1)[1].strip()
            elif line.startswith("Name:"):
                entry["name"] = line.split("Name:", 1)[1].strip()
            elif line.startswith("Description:"):
                entry["description"] = line.split("Description:", 1)[1].strip()
            elif line.startswith("Extended Description:"):
                entry["extendedDescription"] = line.split("Extended Description:", 1)[1].strip()
            elif line.startswith("Embedding:"):
                embedding_str = line.split("Embedding:", 1)[1].strip()
                embedding = json.loads(embedding_str)
            elif not line:
                if entry and embedding:
                    cwe_data.append(entry)
                    embeddings.append(embedding)
                    entry = {}
                    embedding = []
    return cwe_data, embeddings
# Load and parse the CWE data file
def  load_cwe_data_bert():
    cwe_data = []
    embeddings = []
    with open(cwe_data_file_bert, 'r', encoding='utf-8') as f:
        entry = {}
        embedding = []
        for line in f:
            line = line.strip()
            if line.startswith("CWE ID:"):
                entry["cweID"] = line.split("CWE ID:", 1)[1].strip()
            elif line.startswith("Name:"):
                entry["name"] = line.split("Name:", 1)[1].strip()
            elif line.startswith("Description:"):
                entry["description"] = line.split("Description:", 1)[1].strip()
            elif line.startswith("Extended Description:"):
                entry["extendedDescription"] = line.split("Extended Description:", 1)[1].strip()
            elif line.startswith("Embedding:"):
                embedding_str = line.split("Embedding:", 1)[1].strip()
                embedding = json.loads(embedding_str)
            elif not line:
                if entry and embedding:
                    cwe_data.append(entry)
                    embeddings.append(embedding)
                    entry = {}
                    embedding = []
    return cwe_data, embeddings
# Load and parse the CWE data file
def  load_cwe_data_baai():
    cwe_data = []
    embeddings = []
    with open(cwe_data_file_baai, 'r', encoding='utf-8') as f:
        entry = {}
        embedding = []
        for line in f:
            line = line.strip()
            if line.startswith("CWE ID:"):
                entry["cweID"] = line.split("CWE ID:", 1)[1].strip()
            elif line.startswith("Name:"):
                entry["name"] = line.split("Name:", 1)[1].strip()
            elif line.startswith("Description:"):
                entry["description"] = line.split("Description:", 1)[1].strip()
            elif line.startswith("Extended Description:"):
                entry["extendedDescription"] = line.split("Extended Description:", 1)[1].strip()
            elif line.startswith("Embedding:"):
                embedding_str = line.split("Embedding:", 1)[1].strip()
                embedding = json.loads(embedding_str)
            elif not line:
                if entry and embedding:
                    cwe_data.append(entry)
                    embeddings.append(embedding)
                    entry = {}
                    embedding = []
    return cwe_data, embeddings# Load and parse the CWE data file
def  load_cwe_data_e5():
    cwe_data = []
    embeddings = []
    with open(cwe_data_file_e5, 'r', encoding='utf-8') as f:
        entry = {}
        embedding = []
        for line in f:
            line = line.strip()
            if line.startswith("CWE ID:"):
                entry["cweID"] = line.split("CWE ID:", 1)[1].strip()
            elif line.startswith("Name:"):
                entry["name"] = line.split("Name:", 1)[1].strip()
            elif line.startswith("Description:"):
                entry["description"] = line.split("Description:", 1)[1].strip()
            elif line.startswith("Extended Description:"):
                entry["extendedDescription"] = line.split("Extended Description:", 1)[1].strip()
            elif line.startswith("Embedding:"):
                embedding_str = line.split("Embedding:", 1)[1].strip()
                embedding = json.loads(embedding_str)
            elif not line:
                if entry and embedding:
                    cwe_data.append(entry)
                    embeddings.append(embedding)
                    entry = {}
                    embedding = []
    return cwe_data, embeddings
# Load and parse the CWE data file
def  load_cwe_data_labse():
    cwe_data = []
    embeddings = []
    with open(cwe_data_file_labse, 'r', encoding='utf-8') as f:
        entry = {}
        embedding = []
        for line in f:
            line = line.strip()
            if line.startswith("CWE ID:"):
                entry["cweID"] = line.split("CWE ID:", 1)[1].strip()
            elif line.startswith("Name:"):
                entry["name"] = line.split("Name:", 1)[1].strip()
            elif line.startswith("Description:"):
                entry["description"] = line.split("Description:", 1)[1].strip()
            elif line.startswith("Extended Description:"):
                entry["extendedDescription"] = line.split("Extended Description:", 1)[1].strip()
            elif line.startswith("Embedding:"):
                embedding_str = line.split("Embedding:", 1)[1].strip()
                embedding = json.loads(embedding_str)
            elif not line:
                if entry and embedding:
                    cwe_data.append(entry)
                    embeddings.append(embedding)
                    entry = {}
                    embedding = []
    return cwe_data, embeddings
def load_cwe_data_ft_sci_bert():
    cwe_data = []
    embeddings = []
    with open(cwe_data_file_ft_sci_bert, 'r', encoding='utf-8') as f:
        entry = {}
        embedding = []
        for line in f:
            line = line.strip()
            if line.startswith("CWE ID:"):
                entry["cweID"] = line.split("CWE ID:", 1)[1].strip()
            elif line.startswith("Name:"):
                entry["name"] = line.split("Name:", 1)[1].strip()
            elif line.startswith("Description:"):
                entry["description"] = line.split("Description:", 1)[1].strip()
            elif line.startswith("Extended Description:"):
                entry["extendedDescription"] = line.split("Extended Description:", 1)[1].strip()
            elif line.startswith("Embedding:"):
                embedding_str = line.split("Embedding:", 1)[1].strip()
                embedding = json.loads(embedding_str)
            elif not line:
                if entry and embedding:
                    cwe_data.append(entry)
                    embeddings.append(embedding)
                    entry = {}
                    embedding = []
    return cwe_data, embeddings
def load_cwe_data_ft_roberta():
    cwe_data = []
    embeddings = []
    with open(cwe_data_file_ft_roberta, 'r', encoding='utf-8') as f:
        entry = {}
        embedding = []
        for line in f:
            line = line.strip()
            if line.startswith("CWE ID:"):
                entry["cweID"] = line.split("CWE ID:", 1)[1].strip()
            elif line.startswith("Name:"):
                entry["name"] = line.split("Name:", 1)[1].strip()
            elif line.startswith("Description:"):
                entry["description"] = line.split("Description:", 1)[1].strip()
            elif line.startswith("Extended Description:"):
                entry["extendedDescription"] = line.split("Extended Description:", 1)[1].strip()
            elif line.startswith("Embedding:"):
                embedding_str = line.split("Embedding:", 1)[1].strip()
                embedding = json.loads(embedding_str)
            elif not line:
                if entry and embedding:
                    cwe_data.append(entry)
                    embeddings.append(embedding)
                    entry = {}
                    embedding = []
    return cwe_data, embeddings
def load_cwe_data_ft_bert():
    cwe_data = []
    embeddings = []
    with open(cwe_data_file_ft_bert, 'r', encoding='utf-8') as f:
        entry = {}
        embedding = []
        for line in f:
            line = line.strip()
            if line.startswith("CWE ID:"):
                entry["cweID"] = line.split("CWE ID:", 1)[1].strip()
            elif line.startswith("Name:"):
                entry["name"] = line.split("Name:", 1)[1].strip()
            elif line.startswith("Description:"):
                entry["description"] = line.split("Description:", 1)[1].strip()
            elif line.startswith("Extended Description:"):
                entry["extendedDescription"] = line.split("Extended Description:", 1)[1].strip()
            elif line.startswith("Embedding:"):
                embedding_str = line.split("Embedding:", 1)[1].strip()
                embedding = json.loads(embedding_str)
            elif not line:
                if entry and embedding:
                    cwe_data.append(entry)
                    embeddings.append(embedding)
                    entry = {}
                    embedding = []
    return cwe_data, embeddings
def load_cwe_data_ft_sec_bert():
    cwe_data = []
    embeddings = []
    with open(cwe_data_file_ft_sec_bert, 'r', encoding='utf-8') as f:
        entry = {}
        embedding = []
        for line in f:
            line = line.strip()
            if line.startswith("CWE ID:"):
                entry["cweID"] = line.split("CWE ID:", 1)[1].strip()
            elif line.startswith("Name:"):
                entry["name"] = line.split("Name:", 1)[1].strip()
            elif line.startswith("Description:"):
                entry["description"] = line.split("Description:", 1)[1].strip()
            elif line.startswith("Extended Description:"):
                entry["extendedDescription"] = line.split("Extended Description:", 1)[1].strip()
            elif line.startswith("Embedding:"):
                embedding_str = line.split("Embedding:", 1)[1].strip()
                embedding = json.loads(embedding_str)
            elif not line:
                if entry and embedding:
                    cwe_data.append(entry)
                    embeddings.append(embedding)
                    entry = {}
                    embedding = []
    return cwe_data, embeddings
def load_cwe_data_ft_secure_bert():
    cwe_data = []
    embeddings = []
    with open(cwe_data_file_ft_secure_bert, 'r', encoding='utf-8') as f:
        entry = {}
        embedding = []
        for line in f:
            line = line.strip()
            if line.startswith("CWE ID:"):
                entry["cweID"] = line.split("CWE ID:", 1)[1].strip()
            elif line.startswith("Name:"):
                entry["name"] = line.split("Name:", 1)[1].strip()
            elif line.startswith("Description:"):
                entry["description"] = line.split("Description:", 1)[1].strip()
            elif line.startswith("Extended Description:"):
                entry["extendedDescription"] = line.split("Extended Description:", 1)[1].strip()
            elif line.startswith("Embedding:"):
                embedding_str = line.split("Embedding:", 1)[1].strip()
                embedding = json.loads(embedding_str)
            elif not line:
                if entry and embedding:
                    cwe_data.append(entry)
                    embeddings.append(embedding)
                    entry = {}
                    embedding = []
    return cwe_data, embeddings

def load_cwe_data_sci_bert():
    cwe_data = []
    embeddings = []
    with open(cwe_data_file_sci_bert, 'r', encoding='utf-8') as f:
        entry = {}
        embedding = []
        for line in f:
            line = line.strip()
            if line.startswith("CWE ID:"):
                entry["cweID"] = line.split("CWE ID:", 1)[1].strip()
            elif line.startswith("Name:"):
                entry["name"] = line.split("Name:", 1)[1].strip()
            elif line.startswith("Description:"):
                entry["description"] = line.split("Description:", 1)[1].strip()
            elif line.startswith("Extended Description:"):
                entry["extendedDescription"] = line.split("Extended Description:", 1)[1].strip()
            elif line.startswith("Embedding:"):
                embedding_str = line.split("Embedding:", 1)[1].strip()
                embedding = json.loads(embedding_str)
            elif not line:
                if entry and embedding:
                    cwe_data.append(entry)
                    embeddings.append(embedding)
                    entry = {}
                    embedding = []
    return cwe_data, embeddings
def load_cwe_data_secure_bert():
    cwe_data = []
    embeddings = []
    with open(cwe_data_file_securebert, 'r', encoding='utf-8') as f:
        entry = {}
        embedding = []
        for line in f:
            line = line.strip()
            if line.startswith("CWE ID:"):
                entry["cweID"] = line.split("CWE ID:", 1)[1].strip()
            elif line.startswith("Name:"):
                entry["name"] = line.split("Name:", 1)[1].strip()
            elif line.startswith("Description:"):
                entry["description"] = line.split("Description:", 1)[1].strip()
            elif line.startswith("Extended Description:"):
                entry["extendedDescription"] = line.split("Extended Description:", 1)[1].strip()
            elif line.startswith("Embedding:"):
                embedding_str = line.split("Embedding:", 1)[1].strip()
                embedding = json.loads(embedding_str)
            elif not line:
                if entry and embedding:
                    cwe_data.append(entry)
                    embeddings.append(embedding)
                    entry = {}
                    embedding = []
    return cwe_data, embeddings
def load_cwe_data_v2secure_bert():
    cwe_data = []
    embeddings = []
    with open(cwe_data_file_v2securebert, 'r', encoding='utf-8') as f:
        entry = {}
        embedding = []
        for line in f:
            line = line.strip()
            if line.startswith("CWE ID:"):
                entry["cweID"] = line.split("CWE ID:", 1)[1].strip()
            elif line.startswith("Name:"):
                entry["name"] = line.split("Name:", 1)[1].strip()
            elif line.startswith("Description:"):
                entry["description"] = line.split("Description:", 1)[1].strip()
            elif line.startswith("Extended Description:"):
                entry["extendedDescription"] = line.split("Extended Description:", 1)[1].strip()
            elif line.startswith("Embedding:"):
                embedding_str = line.split("Embedding:", 1)[1].strip()
                embedding = json.loads(embedding_str)
            elif not line:
                if entry and embedding:
                    cwe_data.append(entry)
                    embeddings.append(embedding)
                    entry = {}
                    embedding = []
    return cwe_data, embeddings


def load_cwe_data_sec_bert():
    cwe_data = []
    embeddings = []
    with open(cwe_data_file_secbert, 'r', encoding='utf-8') as f:
        entry = {}
        embedding = []
        for line in f:
            line = line.strip()
            if line.startswith("CWE ID:"):
                entry["cweID"] = line.split("CWE ID:", 1)[1].strip()
            elif line.startswith("Name:"):
                entry["name"] = line.split("Name:", 1)[1].strip()
            elif line.startswith("Description:"):
                entry["description"] = line.split("Description:", 1)[1].strip()
            elif line.startswith("Extended Description:"):
                entry["extendedDescription"] = line.split("Extended Description:", 1)[1].strip()
            elif line.startswith("Embedding:"):
                embedding_str = line.split("Embedding:", 1)[1].strip()
                embedding = json.loads(embedding_str)
            elif not line:
                if entry and embedding:
                    cwe_data.append(entry)
                    embeddings.append(embedding)
                    entry = {}
                    embedding = []
    return cwe_data, embeddings

def load_cwe_data_roberta():
    cwe_data = []
    embeddings = []
    with open(cwe_data_file_roberta, 'r', encoding='utf-8') as f:
        entry = {}
        embedding = []
        for line in f:
            line = line.strip()
            if line.startswith("CWE ID:"):
                entry["cweID"] = line.split("CWE ID:", 1)[1].strip()
            elif line.startswith("Name:"):
                entry["name"] = line.split("Name:", 1)[1].strip()
            elif line.startswith("Description:"):
                entry["description"] = line.split("Description:", 1)[1].strip()
            elif line.startswith("Extended Description:"):
                entry["extendedDescription"] = line.split("Extended Description:", 1)[1].strip()
            elif line.startswith("Embedding:"):
                embedding_str = line.split("Embedding:", 1)[1].strip()
                embedding = json.loads(embedding_str)
            elif not line:
                if entry and embedding:
                    cwe_data.append(entry)
                    embeddings.append(embedding)
                    entry = {}
                    embedding = []
    return cwe_data, embeddings
def load_cwe_data_openai():
    # Load CWE data
    with open(cwe_data_file_openai, 'r', encoding='utf-8') as f:
        cwe_data = json.load(f)
    return cwe_data
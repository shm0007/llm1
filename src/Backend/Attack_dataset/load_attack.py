import json
import os
import zipfile

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# File paths for vectorized data
#attack_data_file_bert = 'revectorized_attack_data.txt'
attack_data_file_bert = os.path.join(
    BASE_DIR,
    "revectorized_attack_data.txt"
)


attack_data_file_baai = os.path.join(
    BASE_DIR,
    "baai_revectorized_attack_data.txt"
)
attack_data_file_labse = os.path.join(
    BASE_DIR,
    "labse_revectorized_attack_data.txt"
)
attack_data_file_e5 = os.path.join(
    BASE_DIR,
    "e5_revectorized_attack_data.txt"
)



attack_data_file_gpt_oss = os.path.join(
    BASE_DIR,
    "gpt_oss_revectorized_attack_data.txt"
)



#attack_data_file_openai = 'openai_attack_embeddings.json.zip'
attack_data_file_openai = os.path.join(
    BASE_DIR,
    "openai_attack_embeddings.json.zip"
)

# Load and parse the attack data file
def load_attack_data_bert():
    attack_data = []
    embeddings = []
    with open(attack_data_file_bert, 'r', encoding='utf-8',errors='replace') as f:
        entry = {}
        embedding = []
        for line in f:
            line = line.strip()
            if line.startswith("ID:"):
                entry["attackID"] = line.split("ID:", 1)[1].strip()
            elif line.startswith("Type:"):
                entry["type"] = line.split("Type:", 1)[1].strip()
            elif line.startswith("Name:"):
                entry["name"] = line.split("Name:", 1)[1].strip()
            elif line.startswith("Description:"):
                entry["description"] = line.split("Description:", 1)[1].strip()
            elif line.startswith("Embedding:"):
                embedding_str = line.split("Embedding:", 1)[1].strip()
                embedding = json.loads(embedding_str)
            elif not line:
                if entry and embedding:
                    attack_data.append(entry)
                    embeddings.append(embedding)
                    entry = {}
                    embedding = []
    return attack_data, embeddings

# Load and parse the attack data file
def load_attack_data_baai():
    attack_data = []
    embeddings = []
    with open(attack_data_file_baai, 'r', encoding='utf-8',errors='replace') as f:
        entry = {}
        embedding = []
        for line in f:
            line = line.strip()
            if line.startswith("ID:"):
                entry["attackID"] = line.split("ID:", 1)[1].strip()
            elif line.startswith("Type:"):
                entry["type"] = line.split("Type:", 1)[1].strip()
            elif line.startswith("Name:"):
                entry["name"] = line.split("Name:", 1)[1].strip()
            elif line.startswith("Description:"):
                entry["description"] = line.split("Description:", 1)[1].strip()
            elif line.startswith("Embedding:"):
                embedding_str = line.split("Embedding:", 1)[1].strip()
                embedding = json.loads(embedding_str)
            elif not line:
                if entry and embedding:
                    attack_data.append(entry)
                    embeddings.append(embedding)
                    entry = {}
                    embedding = []
    return attack_data, embeddings

# Load and parse the attack data file
def load_attack_data_e5():
    attack_data = []
    embeddings = []
    with open(attack_data_file_e5, 'r', encoding='utf-8',errors='replace') as f:
        entry = {}
        embedding = []
        for line in f:
            line = line.strip()
            if line.startswith("ID:"):
                entry["attackID"] = line.split("ID:", 1)[1].strip()
            elif line.startswith("Type:"):
                entry["type"] = line.split("Type:", 1)[1].strip()
            elif line.startswith("Name:"):
                entry["name"] = line.split("Name:", 1)[1].strip()
            elif line.startswith("Description:"):
                entry["description"] = line.split("Description:", 1)[1].strip()
            elif line.startswith("Embedding:"):
                embedding_str = line.split("Embedding:", 1)[1].strip()
                embedding = json.loads(embedding_str)
            elif not line:
                if entry and embedding:
                    attack_data.append(entry)
                    embeddings.append(embedding)
                    entry = {}
                    embedding = []
    return attack_data, embeddings

# Load and parse the attack data file
def load_attack_data_labse():
    attack_data = []
    embeddings = []
    with open(attack_data_file_labse, 'r', encoding='utf-8',errors='replace') as f:
        entry = {}
        embedding = []
        for line in f:
            line = line.strip()
            if line.startswith("ID:"):
                entry["attackID"] = line.split("ID:", 1)[1].strip()
            elif line.startswith("Type:"):
                entry["type"] = line.split("Type:", 1)[1].strip()
            elif line.startswith("Name:"):
                entry["name"] = line.split("Name:", 1)[1].strip()
            elif line.startswith("Description:"):
                entry["description"] = line.split("Description:", 1)[1].strip()
            elif line.startswith("Embedding:"):
                embedding_str = line.split("Embedding:", 1)[1].strip()
                embedding = json.loads(embedding_str)
            elif not line:
                if entry and embedding:
                    attack_data.append(entry)
                    embeddings.append(embedding)
                    entry = {}
                    embedding = []
    return attack_data, embeddings

def load_attack_data_gpt_oss():
    attack_data = []
    embeddings = []
    with open(attack_data_file_gpt_oss, 'r', encoding='utf-8',errors='replace') as f:
        entry = {}
        embedding = []
        for line in f:
            line = line.strip()
            if line.startswith("ID:"):
                entry["attackID"] = line.split("ID:", 1)[1].strip()
            elif line.startswith("Type:"):
                entry["type"] = line.split("Type:", 1)[1].strip()
            elif line.startswith("Name:"):
                entry["name"] = line.split("Name:", 1)[1].strip()
            elif line.startswith("Description:"):
                entry["description"] = line.split("Description:", 1)[1].strip()
            elif line.startswith("Embedding:"):
                embedding_str = line.split("Embedding:", 1)[1].strip()
                embedding = json.loads(embedding_str)
            elif not line:
                if entry and embedding:
                    attack_data.append(entry)
                    embeddings.append(embedding)
                    entry = {}
                    embedding = []
    return attack_data, embeddings


def load_attack_data_openai():
    attack_data = []
    # Unzip and load Attack data
    if attack_data_file_openai.endswith('.zip'):
        extracted_dir = '/tmp/extracted_attack_data'  # Temporary directory for extracted files
        os.makedirs(extracted_dir, exist_ok=True)
        
        with zipfile.ZipFile(attack_data_file_openai, 'r') as zip_ref:
            zip_ref.extractall(extracted_dir)
        
        # Assuming the JSON file is the only file in the zip or has a known name
        extracted_files = os.listdir(extracted_dir)
        extracted_json_file = [file for file in extracted_files if file.endswith('.json')][0]
        extracted_json_path = os.path.join(extracted_dir, extracted_json_file)
        
        with open(extracted_json_path, 'r', encoding='utf-8') as f:
            attack_data = json.load(f)
    else:
        with open(attack_data_file_openai, 'r', encoding='utf-8') as f:
            attack_data = json.load(f)
    return attack_data
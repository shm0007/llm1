import re
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics.pairwise import cosine_similarity

# -------------------------------------------------------
# 1. Read and Parse the Embeddings from Your TXT File
# -------------------------------------------------------
def load_embeddings_from_textfile(path):
    embeddings = []

    with open(path, "r", encoding="latin-1") as f:
        text = f.read()

    # Regex to extract the vector inside brackets after "Embedding:"
    pattern = r"Embedding:\s*\[([^\]]+)\]"
    matches = re.findall(pattern, text)

    for m in matches:
        # convert string: "-0.23, 0.12, 0.88" → list of floats
        vec = np.array([float(x.strip()) for x in m.split(",")])
        embeddings.append(vec)

    return np.array(embeddings)


file_path = "revectorized_attack_data.txt"
#file_path = "vectorized_cwe_data.txt"

stored_embeddings = load_embeddings_from_textfile(file_path)
print("Loaded embeddings:", stored_embeddings.shape)   # (N, 768)
from transformers import BertTokenizer, BertModel
import torch

tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
model = BertModel.from_pretrained("bert-base-uncased")
model.eval()

def get_bert_embedding(text):
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    model = BertModel.from_pretrained('bert-base-uncased')
    
    inputs = tokenizer(text, return_tensors='pt', truncation=True, max_length=512, padding=True)
    outputs = model(**inputs)
    return outputs.last_hidden_state.mean(dim=1).squeeze().detach().numpy()

#query_text = "When I open outside URLs without isolating them, the new page can tamper with my original tab. I may return thinking nothing changed, unaware the page has been swapped with a look-alike asking for sensitive info"
query_text = "We’re seeing an issue where any text entered into the profile ‘About Me’ section is rendered directly on the page without sanitization. If a user types <script>alert('test')</script>, it actually pops up for anyone visiting the profile. Can you check what we’re missing on the output encoding? "
query_embedding = get_bert_embedding(query_text)
query_vector = query_embedding.reshape(1, -1)
similarities = cosine_similarity(query_vector, stored_embeddings)[0]

print("First 10 similarities:", similarities[:10])
plt.figure(figsize=(8, 5))
plt.hist(similarities, bins=40, edgecolor="black",range=(0, 1))
plt.title("Cosine Similarity Distribution with ATT&CK Embeddings")
plt.xlabel("Cosine Similarity")
plt.ylabel("Count")
plt.xlim(0, 1) 
plt.grid(axis="y", alpha=0.3)
plt.show()

import torch
from transformers import BertTokenizer, BertModel
from pathlib import Path
from transformers import AutoTokenizer, AutoModel

import json

class GenerateEmbeddings:
    def __init__(self, input_file, output_file):
        self.input_file = Path(input_file)  # Ensure Path object
        self.output_file = Path(output_file)  # Ensure Path object

        # Load RoBERTa model and tokenizer
        self.tokenizer = AutoTokenizer.from_pretrained("jackaduma/SecBERT")
        self.model = AutoModel.from_pretrained("jackaduma/SecBERT")


        # Check if input file exists
        if not self.input_file.exists():
            print(f"Input file not found: {self.input_file}")
            return

        print(f"Generating embeddings for: {self.input_file}")

        # Read the cleaned data
        cleaned_data = self._read_cleaned_data()

        # Generate and save embeddings
        self._generate_and_save_embeddings(cleaned_data)

    def _read_cleaned_data(self):
        # Read the cleaned data file and extract the fields
        entries = []
        entry = {}
        with open(self.input_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line.startswith("File:"):
                    entry["file"] = line.replace("File: ", "")
                elif line.startswith("ID:"):
                    entry["id"] = line.replace("ID: ", "")
                elif line.startswith("Type:"):
                    entry["type"] = line.replace("Type: ", "")
                elif line.startswith("Name:"):
                    entry["name"] = line.replace("Name: ", "")
                elif line.startswith("Description:"):
                    entry["description"] = line.replace("Description: ", "")
                elif line == "":  # End of an entry
                    if entry:
                        entries.append(entry)
                        entry = {}
        return entries

    def _generate_and_save_embeddings(self, data):
        # Generate embeddings and save to the output file
        with open(self.output_file, 'w') as f:
            for entry in data:
                # Prepare the text to embed
                text_to_embed = f"{entry['file']} {entry['id']} {entry['type']} {entry['name']} {entry['description']}"
                inputs = self.tokenizer(
                    text_to_embed, 
                    return_tensors='pt', 
                    truncation=True, 
                    max_length=512, 
                    padding=True
                )
                outputs = self.model(**inputs)
                # Use the [CLS] token embedding as the sentence embedding
                cls_embedding = outputs.last_hidden_state[:, 0, :].squeeze(0).tolist()
                
                # Format and write the entry to the output file
                f.write(f"File: {entry['file']}\n")
                f.write(f"ID: {entry['id']}\n")
                f.write(f"Type: {entry['type']}\n")
                f.write(f"Name: {entry['name']}\n")
                f.write(f"Description: {entry['description']}\n")
                f.write(f"Embedding: {cls_embedding}\n\n")  # Leave a blank line between entries
        print(f"Embeddings saved to {self.output_file}")

# Pass explicit paths for input and output files
input_path = "cleaned_attack_data.txt"
output_path = "secbert_revectorized_attack_data.txt"

# Run the GenerateEmbeddings class with specified paths
GenerateEmbeddings(input_file=input_path, output_file=output_path)

import torch
from transformers import BertTokenizer, BertModel,AutoTokenizer,AutoModel
from pathlib import Path

class GenerateCWEEmbeddings:
    def __init__(self, input_file, output_file):
        self.input_file = Path(input_file)
        self.output_file = Path(output_file)

        # Load model + tokenizer
        self.tokenizer = AutoTokenizer.from_pretrained("jackaduma/SecBERT")
        self.model = AutoModel.from_pretrained("jackaduma/SecBERT")
    def _get_embedding(self, text):
        inputs = self.tokenizer(text, return_tensors="pt", truncation=True, max_length=512, padding=True)
        with torch.no_grad():
            outputs = self.model(**inputs)
        return outputs.last_hidden_state.mean(dim=1).squeeze().tolist()

    def _parse_cwe_file(self):
        with open(self.input_file, "r", encoding="utf-8",errors="replace") as f:
            raw = f.read().strip()

        # Split by CWE blocks (double newlines separate entries)
        entries = raw.split("\n\n")

        parsed = []
        for entry in entries:
            lines = entry.strip().split("\n")
            print(f"----------\n{lines}\n------------".encode("utf-8", errors="replace"))
            cwe_id = lines[0].replace("ID:", "").strip()
            name = lines[1].replace("Name:", "").strip()
            description = lines[2].replace("Description:", "").strip()
            extended_desc = lines[3].replace("Extended Description:", "").strip()

            text = f"{cwe_id} {name} {description} {extended_desc}"
            parsed.append({"id": cwe_id, "name": name, "text": text, "description": description, "extended_desc": extended_desc})
        return parsed

    def generate_and_save(self):
        parsed_entries = self._parse_cwe_file()
        with open(self.output_file, "w", encoding="utf-8") as f:
            for entry in parsed_entries:
                print(entry["id"],flush=True)
                emb = self._get_embedding(entry["text"])
                f.write(f"CWE ID: {entry['id']}\n")
                f.write(f"Name: {entry['name']}\n")
                f.write(f"Description: {entry['description']}\n")
                f.write(f"Extended Description: {entry['extended_desc']}\n")
                f.write(f"Embedding: {emb}\n\n")

if __name__ == "__main__":
    input_path = "formatted_cwe_entries.txt"
    output_path = "cwe_sec_bert_embeddings.txt"
    generator = GenerateCWEEmbeddings(input_path, output_path)
    generator.generate_and_save()

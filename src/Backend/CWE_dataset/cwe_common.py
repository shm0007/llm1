import torch
from transformers import AutoTokenizer, AutoModel
from pathlib import Path
import argparse


class GenerateCWEEmbeddings:
    def __init__(self, input_file, output_file, model_name):
        self.input_file = Path(input_file)
        self.output_file = Path(output_file)
        self.model_name = model_name

        # Load model + tokenizer (UNCHANGED behavior)
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModel.from_pretrained(self.model_name)
        self.model.eval()

    def _maybe_add_e5_prefix(self, text: str) -> str:
        # ONLY change for E5 models
        if self.model_name.startswith("intfloat/e5"):
            return f"passage: {text}"
        return text

    def _get_embedding(self, text):
        text = self._maybe_add_e5_prefix(text)

        inputs = self.tokenizer(
            text,
            return_tensors="pt",
            truncation=True,
            max_length=512,
            padding=True,
        )
        with torch.no_grad():
            outputs = self.model(**inputs)

        # ✅ EXACT SAME pooling as your original code
        return outputs.last_hidden_state.mean(dim=1).squeeze().tolist()

    def _parse_cwe_file(self):
        with open(self.input_file, "r", encoding="utf-8", errors="replace") as f:
            raw = f.read().strip()

        entries = raw.split("\n\n")
        parsed = []

        for entry in entries:
            lines = entry.strip().split("\n")
            if len(lines) < 4:
                continue

            cwe_id = lines[0].replace("ID:", "").strip()
            name = lines[1].replace("Name:", "").strip()
            description = lines[2].replace("Description:", "").strip()
            extended_desc = lines[3].replace("Extended Description:", "").strip()

            text = f"{cwe_id} {name} {description} {extended_desc}"
            parsed.append({
                "id": cwe_id,
                "name": name,
                "text": text,
                "description": description,
                "extended_desc": extended_desc,
            })

        return parsed

    def generate_and_save(self):
        parsed_entries = self._parse_cwe_file()
        with open(self.output_file, "w", encoding="utf-8") as f:
            for entry in parsed_entries:
                print(entry["id"], flush=True)
                emb = self._get_embedding(entry["text"])

                f.write(f"CWE ID: {entry['id']}\n")
                f.write(f"Name: {entry['name']}\n")
                f.write(f"Description: {entry['description']}\n")
                f.write(f"Extended Description: {entry['extended_desc']}\n")
                f.write(f"Embedding: {emb}\n\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate CWE embeddings (BGE / E5)")
    
    parser.add_argument("--output", required=True, help="Output embedding file")
    parser.add_argument("--model", required=True, help="HF model name")

    args = parser.parse_args()

    generator = GenerateCWEEmbeddings(
        input_file='formatted_cwe_entries.txt',
        output_file=args.output,
        model_name=args.model,
    )
    generator.generate_and_save()

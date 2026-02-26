import argparse
from pathlib import Path
import torch
from transformers import AutoTokenizer, AutoModel


class GenerateEmbeddings:
    def __init__(self, input_file, output_file, model_name):
        self.input_file = Path(input_file)
        self.output_file = Path(output_file)
        self.model_name = model_name

        if not self.input_file.exists():
            raise FileNotFoundError(f"Input file not found: {self.input_file}")

        print(f"Loading model: {self.model_name}")

        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModel.from_pretrained(self.model_name)
        self.model.eval()

        print(f"Generating embeddings for: {self.input_file}")

        data = self._read_cleaned_data()
        self._generate_and_save_embeddings(data)

    def _read_cleaned_data(self):
        entries = []
        entry = {}

        with open(self.input_file, "r", encoding="utf-8") as f:
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
                elif line == "":
                    if entry:
                        entries.append(entry)
                        entry = {}

        if entry:
            entries.append(entry)

        return entries

    def _generate_and_save_embeddings(self, data):
        with open(self.output_file, "w", encoding="utf-8") as f, torch.no_grad():
            for entry in data:
                text = f"{entry['file']} {entry['id']} {entry['type']} {entry['name']} {entry['description']}"

                # ---- E5 models REQUIRE a prefix ----
                if self.model_name.startswith("intfloat/e5"):
                    text = f"passage: {text}"

                inputs = self.tokenizer(
                    text,
                    return_tensors="pt",
                    truncation=True,
                    max_length=512,
                    padding=True,
                )

                outputs = self.model(**inputs)

                # CLS token embedding (same as your BAAI script)
                embedding = outputs.last_hidden_state[:, 0, :].squeeze(0)

                f.write(f"File: {entry['file']}\n")
                f.write(f"ID: {entry['id']}\n")
                f.write(f"Type: {entry['type']}\n")
                f.write(f"Name: {entry['name']}\n")
                f.write(f"Description: {entry['description']}\n")
                f.write(f"Embedding: {embedding.tolist()}\n\n")

        print(f"Embeddings saved to {self.output_file}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate embeddings for ATT&CK/CWE text")
    parser.add_argument("--output", required=True, help="Output embedding file")
    parser.add_argument(
        "--model",
        required=True,
        help="HuggingFace model name (e.g. intfloat/e5-base-v2, BAAI/bge-large-en-v1.5)",
    )

    args = parser.parse_args()

    GenerateEmbeddings(
        input_file='cleaned_attack_data.txt',
        output_file=args.output,
        model_name=args.model,
    )

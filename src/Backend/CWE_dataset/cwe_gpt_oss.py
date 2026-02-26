import torch
from pathlib import Path
from transformers import AutoTokenizer, AutoModelForCausalLM


class GenerateCWEEmbeddings:
    def __init__(
        self,
        input_file,
        output_file,
        model_id="openai/gpt-oss-20b",
        batch_size=8,
        max_length=512,
        normalize=True,
    ):
        self.input_file = Path(input_file)
        self.output_file = Path(output_file)
        self.model_id = model_id
        self.batch_size = int(batch_size)
        self.max_length = int(max_length)
        self.normalize = bool(normalize)

        # Load tokenizer + model
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_id)
        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token

        dtype = torch.bfloat16 if torch.cuda.is_available() else torch.float32
        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_id,
            device_map="auto",
            torch_dtype=dtype,
        )
        self.model.eval()

        if not self.input_file.exists():
            raise FileNotFoundError(f"Input file not found: {self.input_file}")

    @staticmethod
    def _masked_mean_pool(last_hidden_state: torch.Tensor, attention_mask: torch.Tensor) -> torch.Tensor:
        """
        last_hidden_state: (B, T, H)
        attention_mask:    (B, T)
        returns:           (B, H)
        """
        mask = attention_mask.unsqueeze(-1).to(last_hidden_state.dtype)  # (B, T, 1)
        summed = (last_hidden_state * mask).sum(dim=1)                   # (B, H)
        denom = mask.sum(dim=1).clamp(min=1e-9)                          # (B, 1)
        return summed / denom

    def _parse_cwe_file(self):
        """
        Expected format per entry (separated by blank line):
        ID: ...
        Name: ...
        Description: ...
        Extended Description: ...
        """
        with open(self.input_file, "r", encoding="utf-8", errors="replace") as f:
            raw = f.read().strip()

        entries = raw.split("\n\n")
        parsed = []

        for entry in entries:
            lines = [ln.strip() for ln in entry.strip().split("\n") if ln.strip()]
            if len(lines) < 4:
                # Skip malformed blocks instead of crashing
                continue

            cwe_id = lines[0].replace("ID:", "").strip()
            name = lines[1].replace("Name:", "").strip()
            description = lines[2].replace("Description:", "").strip()
            extended_desc = lines[3].replace("Extended Description:", "").strip()

            text = f"{cwe_id} {name} {description} {extended_desc}"
            parsed.append(
                {
                    "id": cwe_id,
                    "name": name,
                    "text": text,
                    "description": description,
                    "extended_desc": extended_desc,
                }
            )

        return parsed

    def generate_and_save(self):
        parsed_entries = self._parse_cwe_file()
        if not parsed_entries:
            print("No valid CWE entries found. Check input formatting.")
            return

        model_device = next(self.model.parameters()).device

        with open(self.output_file, "w", encoding="utf-8") as f, torch.no_grad():
            for start in range(0, len(parsed_entries), self.batch_size):
                batch_entries = parsed_entries[start : start + self.batch_size]
                batch_texts = [e["text"] for e in batch_entries]

                inputs = self.tokenizer(
                    batch_texts,
                    return_tensors="pt",
                    truncation=True,
                    max_length=self.max_length,
                    padding=True,
                )
                inputs = {k: v.to(model_device) for k, v in inputs.items()}

                outputs = self.model(**inputs, output_hidden_states=True, return_dict=True)
                last_hidden = outputs.hidden_states[-1]  # (B, T, H)

                emb = self._masked_mean_pool(last_hidden, inputs["attention_mask"])  # (B, H)

                if self.normalize:
                    emb = torch.nn.functional.normalize(emb, p=2, dim=-1)

                emb = emb.float().cpu()

                for entry, vec in zip(batch_entries, emb):
                    print(entry["id"], flush=True)
                    f.write(f"CWE ID: {entry['id']}\n")
                    f.write(f"Name: {entry['name']}\n")
                    f.write(f"Description: {entry['description']}\n")
                    f.write(f"Extended Description: {entry['extended_desc']}\n")
                    f.write(f"Embedding: {vec.tolist()}\n\n")

        print(f"Embeddings saved to {self.output_file}")


if __name__ == "__main__":
    input_path = "formatted_cwe_entries.txt"
    output_path = "cwe_gpt_oss_embeddings.txt"

    generator = GenerateCWEEmbeddings(
        input_file=input_path,
        output_file=output_path,
        model_id="openai/gpt-oss-20b",
        batch_size=8,     # tune if OOM
        max_length=512,   # tune if OOM
        normalize=True,   # good for cosine similarity
    )
    generator.generate_and_save()

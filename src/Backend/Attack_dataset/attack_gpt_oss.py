import torch
from pathlib import Path
from transformers import AutoTokenizer, AutoModelForCausalLM

class GenerateEmbeddings:
    def __init__(self, input_file, output_file, model_id="openai/gpt-oss-20b"):
        self.input_file = Path(input_file)
        self.output_file = Path(output_file)

        # ---- Load GPT-OSS ----
        self.tokenizer = AutoTokenizer.from_pretrained(model_id)

        # Some causal LMs don't ship with a pad token. Ensure one exists for padding.
        if self.tokenizer.pad_token is None:
            # Prefer eos as pad token for causal LMs
            self.tokenizer.pad_token = self.tokenizer.eos_token

        # Use bfloat16 on supported GPUs; otherwise float32 on CPU.
        dtype = torch.bfloat16 if torch.cuda.is_available() else torch.float32

        self.model = AutoModelForCausalLM.from_pretrained(
            model_id,
            device_map="auto",     # spreads across available GPU(s) / CPU
            torch_dtype=dtype,
        )
        self.model.eval()

        if not self.input_file.exists():
            raise FileNotFoundError(f"Input file not found: {self.input_file}")

        print(f"Generating embeddings for: {self.input_file}")
        cleaned_data = self._read_cleaned_data()
        self._generate_and_save_embeddings(cleaned_data)

    def _read_cleaned_data(self):
        entries = []
        entry = {}
        with open(self.input_file, "r", encoding="utf-8") as f:
            for raw_line in f:
                line = raw_line.strip()
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

        # Handle case where file doesn't end with a blank line
        if entry:
            entries.append(entry)

        return entries

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

    def _generate_and_save_embeddings(self, data, max_length=512, normalize=True):
        with open(self.output_file, "w", encoding="utf-8") as f, torch.no_grad():
            for entry in data:
                text_to_embed = f"{entry['file']} {entry['id']} {entry['type']} {entry['name']} {entry['description']}"

                inputs = self.tokenizer(
                    text_to_embed,
                    return_tensors="pt",
                    truncation=True,
                    max_length=max_length,
                    padding=True,
                )

                # With device_map="auto", model may be on GPU; send inputs to the model's first device.
                # This works for common single-device / auto setups.
                model_device = next(self.model.parameters()).device
                inputs = {k: v.to(model_device) for k, v in inputs.items()}

                outputs = self.model(**inputs, output_hidden_states=True, return_dict=True)
                # Use the LAST hidden layer from hidden_states
                last_hidden = outputs.hidden_states[-1]  # (B, T, H)

                emb = self._masked_mean_pool(last_hidden, inputs["attention_mask"])  # (B, H)

                if normalize:
                    emb = torch.nn.functional.normalize(emb, p=2, dim=-1)

                embedding_list = emb.squeeze(0).float().cpu().tolist()

                f.write(f"File: {entry.get('file','')}\n")
                f.write(f"ID: {entry.get('id','')}\n")
                f.write(f"Type: {entry.get('type','')}\n")
                f.write(f"Name: {entry.get('name','')}\n")
                f.write(f"Description: {entry.get('description','')}\n")
                f.write(f"Embedding: {embedding_list}\n\n")

        print(f"Embeddings saved to {self.output_file}")


# Paths
input_path = "cleaned_attack_data.txt"
output_path = "gpt_oss_revectorized_attack_data.txt"

GenerateEmbeddings(input_file=input_path, output_file=output_path)

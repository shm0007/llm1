# attacks_parser_to_txt.py  (patched _extract_relevant_data)
import json
from pathlib import Path

MITRE_SOURCES = {"mitre-attack", "mitre-ics-attack", "mitre-mobile-attack"}

class CleanData:
    def __init__(self):
        self.base_dir = Path('C:\\ACodes\\cwe\\datasets\\json')
        self.subdirectories = ["enterprise-attack", "ics-attack", "mobile-attack"]
        self.allowed_folders = {"attack-pattern", "course-of-action", "malware"}
        self.cleaned_data = []

        if not self.base_dir.exists():
            print(f"Base directory not found: {self.base_dir}")
            return

        print("Starting dataset cleaning...")
        for subdirectory_name in self.subdirectories:
            subdirectory = self.base_dir / subdirectory_name
            if subdirectory.is_dir():
                for json_file in self._get_all_json_files(subdirectory):
                    print(f"Loading JSON file: {json_file}")
                    content = self._load_json(json_file)
                    if content:
                        self._extract_relevant_data(json_file.name, content)

        self._save_cleaned_data_to_txt()

    def _get_all_json_files(self, directory):
        json_files = []
        for subfolder in directory.iterdir():
            if subfolder.is_dir() and subfolder.name in self.allowed_folders:
                json_files.extend(list(subfolder.rglob('*.json')))
        print(f"Found {len(json_files)} JSON files in {directory}")
        return json_files

    def _load_json(self, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError:
            print(f"JSON decoding error in file: {file_path}")
            return None

    def _mitre_external_id(self, obj):
        for ref in obj.get("external_references", []) or []:
            src = (ref.get("source_name") or "").lower()
            ext_id = ref.get("external_id")
            if src in MITRE_SOURCES and ext_id:
                return ext_id.strip()  # e.g., "T1059" or "T1059.003"
        return None

    def _extract_relevant_data(self, file_name, content):
        objects = content.get('objects', [])
        print(f"Extracted {len(objects)} objects from {file_name}")
        for obj in objects:
            # optional: only keep ATT&CK patterns for the attack corpus
            # if obj.get('type') != 'attack-pattern': 
            #     continue
            mitre_id = self._mitre_external_id(obj)
            entry = {
                "file": file_name,
                # Use MITRE external_id if present; else fall back to STIX object id
                "id": mitre_id or obj.get('id', 'N/A'),
                "type": obj.get('type', 'N/A'),
                "name": obj.get('name', 'N/A'),
                "description": obj.get('description', 'N/A'),
            }
            self.cleaned_data.append(entry)

    def _save_cleaned_data_to_txt(self):
        output_file_path = "cleaned_attack_data.txt"
        with open(output_file_path, 'w', encoding='utf-8') as txt_file:
            for e in self.cleaned_data:
                txt_file.write(
                    f"File: {e['file']}\n"
                    f"ID: {e['id']}\n"
                    f"Type: {e['type']}\n"
                    f"Name: {e['name']}\n"
                    f"Description: {e['description']}\n\n"
                )
        print(f"Cleaned data saved to {output_file_path}")

if __name__ == "__main__":
    CleanData()

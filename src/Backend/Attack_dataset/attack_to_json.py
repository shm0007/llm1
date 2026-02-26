import re
from pathlib import Path
import json

def parse_attack_file_text(path):
    """
    Parse a text file that contains one-or-more blocks like:
      File: attack-pattern--....json
      ID: T1055.011
      Type: attack-pattern
      Name: Extra Window Memory Injection
      Description: <multi-line description...>

    Returns:
      dict: { attack_id: {"name": name_str, "description": desc_str}, ... }
    """
    text = Path(path).read_text(encoding="utf-8")

    # Regex pattern:
    # - non-greedy match for Name
    # - Description is captured in DOTALL mode until next "File:" or EOF
    pattern = re.compile(
        r"""           # verbose regex
        File:\s*.*?\.json\s*   # the 'File: ...json' line (skip)
        \s*ID:\s*(?P<id>\S+)\s*    # ID: <id>
        \s*Type:\s*(?P<type>.*?)\s* # Type: <type>  (we capture but don't use)
        \s*Name:\s*(?P<name>.*?)\s* # Name: <name>
        \s*Description:\s*(?P<desc>.*?)   # Description: <multi-line desc>
        (?=\nFile:\s*.*?\.json|\Z)        # stop at next File: or EOF
        """,
        re.IGNORECASE | re.DOTALL | re.VERBOSE,
    )

    out = {}
    for m in pattern.finditer(text):
        aid = m.group("id").strip()
        name = " ".join(m.group("name").split())  # normalize whitespace
        desc = m.group("desc").strip()
        # normalize internal whitespace and preserve paragraphs
        # replace multiple consecutive newlines with two newlines, and strip lines
        desc_lines = [line.rstrip() for line in desc.splitlines()]
        # join with single newline, then collapse runs of >2 newlines to two
        desc = "\n".join(desc_lines).strip()
        desc = re.sub(r"\n{3,}", "\n\n", desc)
        out[aid] = {"name": name, "description": desc}

    return out

# Example usage:
if __name__ == "__main__":
    attacks = parse_attack_file_text("cleaned_attack_data.txt")
    print(f"Found {len(attacks)} attacks. Example:")
    for k in list(attacks)[:3]:
        print(k, attacks[k]["name"])
    # Save to JSON for later lookup
cleaned = json.dumps(attacks, indent=2, ensure_ascii=False)
Path("attacks_index.json").write_text(cleaned.encode("utf-8", "ignore").decode("utf-8"), encoding="utf-8")

print("Saved attacks_index.json")

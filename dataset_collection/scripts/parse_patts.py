# dataset_collection/scripts/parse_patts.py

import os
import json

BASE_DIR = "../raw_data/PATTs"  # Adjust path as needed
OUTPUT_FILE = "../processed/patts_extracted.jsonl"

def extract_payloads_from_markdown(markdown_file, vuln_type):
    """
    Read a Markdown file line by line, 
    return payloads that appear relevant for the vulnerability type.
    """
    payloads = []
    with open(markdown_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            # Simple heuristic: skip headings or empty lines
            if line.startswith("#") or not line:
                continue
            # Add other logic if you only want lines containing code/payload
            # For example, skip lines without any special chars
            # Or parse bullet points that start with `- `
            if any(symbol in line for symbol in ["<script>", "'", "../../", "http://"]):
                payloads.append(line)
    # Convert them into a structured list of dicts
    result = []
    for p in payloads:
        result.append({
            "vulnerability_type": vuln_type,
            "payload": p,
            "source": "PayloadsAllTheThings"
        })
    return result

def main():
    all_data = []
    # Map folder/file to vulnerability types
    vuln_folders = {
        "SQL Injection": "sql_injection",
        "XSS": "xss",
        "LFI": "lfi",
        "SSRF": "ssrf"
        # Add more as needed
    }

    for folder_name, vuln_type in vuln_folders.items():
        folder_path = os.path.join(BASE_DIR, folder_name)
        if os.path.isdir(folder_path):
            for file in os.listdir(folder_path):
                if file.endswith(".md"):
                    file_path = os.path.join(folder_path, file)
                    extracted = extract_payloads_from_markdown(file_path, vuln_type)
                    all_data.extend(extracted)

    # Write out to JSONL
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as out:
        for record in all_data:
            out.write(json.dumps(record) + "\n")

    print(f"Done! Extracted {len(all_data)} payloads to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
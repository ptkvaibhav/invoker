import re
import json
import glob

data_samples = []

# Read all Markdown reports
for file in glob.glob("Awesome-Bugbounty-Writeups/**/*.md", recursive=True):
    with open(file, "r", encoding="utf-8") as f:
        content = f.read()

    # Extract Title (first line of Markdown)
    title_match = re.search(r"# (.+)", content)
    title = title_match.group(1) if title_match else "Unknown Title"

    # Extract Vulnerability Type from Keywords
    vulnerability_type = "Other"
    if "XSS" in title.upper():
        vulnerability_type = "XSS"
    elif "SQLi" in title.upper():
        vulnerability_type = "SQLi"
    elif "SSRF" in title.upper():
        vulnerability_type = "SSRF"
    elif "IDOR" in title.upper():
        vulnerability_type = "IDOR"
    elif "LFI" in title.upper():
        vulnerability_type = "LFI"

    # Extract Code Blocks (Contains HTTP requests, payloads)
    code_blocks = re.findall(r"```(?:http|html|js|php|sql)?\n(.*?)```", content, re.DOTALL)
    
    # Extract Payloads from Code Blocks
    payloads = [block.strip() for block in code_blocks if len(block.strip()) > 5]

    # Extract Description (First paragraph after the title)
    description_match = re.search(r"\n\n(.+?)\n\n", content, re.DOTALL)
    description = description_match.group(1).strip() if description_match else "No Description"

    # Store Extracted Data
    data_samples.append({
        "title": title,
        "type": vulnerability_type,
        "description": description,
        "payloads": payloads
    })

# Save Extracted Reports
with open("bugbounty_reports_fixed.jsonl", "w", encoding="utf-8") as f:
    for entry in data_samples:
        f.write(json.dumps(entry) + "\n")

print(f"✅ Successfully extracted {len(data_samples)} bug bounty reports!")
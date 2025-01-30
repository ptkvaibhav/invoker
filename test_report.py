import json

with open("bugbounty_reports_fixed.jsonl", "r") as f:
    for i in range(5):
        print(json.loads(f.readline()))
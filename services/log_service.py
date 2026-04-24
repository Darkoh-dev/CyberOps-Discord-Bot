import json


RULES_PATH = "data/sample_rules.json"


def load_log_rules():
    with open(RULES_PATH, "r", encoding="utf-8") as rules_files:
        data = json.load(rules_files)

        return data.get("rules", [])
    

def analyze_log_text(log_text):
    rules = load_log_rules()
    normalized_text = log_text.lower()
    findings = []

    for rule in rules:
        pattern = rule.get("pattern", "").lower()

        if pattern and pattern in normalized_text:
            findings.append(
                {
                    "name": rule["name"],
                    "severity": rule["severity"],
                    "description": rule["description"]
                }
            )

    return findings
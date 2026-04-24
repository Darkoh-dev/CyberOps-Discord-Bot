import json


FEEDS_PATH = "config/feeds.json"


def load_threat_items():
    with open(FEEDS_PATH, "r", encoding="utf-8") as feeds_file:
        data = json.load(feeds_file)

    return data.get("threat_items", [])


def get_threat_items(category=None, severity=None, limit=5):
    items = load_threat_items()

    if category:
        items = [
            item for item in items
            if item.get("category", "").lower() == category.lower()
        ]

    if severity:
        items = [
            item for item in items
            if item.get("severity", "").lower() == severity.lower()
        ]

    return items[:limit]
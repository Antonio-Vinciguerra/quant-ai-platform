import os
import json
import hashlib
from datetime import datetime
from collections import defaultdict

RAW_DIR = os.path.expanduser("~/quant-ai-platform/knowledge_base/raw_scraped")
CLEANED_DIR = os.path.expanduser("~/quant-ai-platform/knowledge_base/cleaned")
LOG_FILE = os.path.expanduser("~/quant-ai-platform/logs/cleaning.log")
REPORT_FILE = os.path.expanduser("~/quant-ai-platform/logs/cleaning_report.json")

os.makedirs(CLEANED_DIR, exist_ok=True)
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

def content_hash(item):
    string = json.dumps(item, sort_keys=True)
    return hashlib.md5(string.encode("utf-8")).hexdigest()

deduplicated_data = defaultdict(dict)
report = {
    "timestamp": datetime.utcnow().isoformat(),
    "files_scanned": 0,
    "total_items_before": 0,
    "total_items_after": 0,
    "duplicates_removed": 0,
    "cleaned_files_created": 0
}

for filename in os.listdir(RAW_DIR):
    if not filename.endswith(".json"):
        continue
    filepath = os.path.join(RAW_DIR, filename)
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception:
        continue

    report["files_scanned"] += 1

    # Handle legacy flat list files
    if isinstance(data, list):
        source = "unknown"
        articles = data
    elif isinstance(data, dict):
        source = data.get("source", "unknown")
        articles = data.get("articles") or data.get("items") or []
    else:
        continue  # Skip unknown formats

    report["total_items_before"] += len(articles)

    for item in articles:
        h = content_hash(item)
        if h not in deduplicated_data[source]:
            deduplicated_data[source][h] = item

for source, items in deduplicated_data.items():
    cleaned_list = list(items.values())
    report["total_items_after"] += len(cleaned_list)
    filename = f"cleaned_{source}_{datetime.utcnow().strftime('%Y%m%dT%H%M%S')}.json"
    path = os.path.join(CLEANED_DIR, filename)
    with open(path, "w", encoding="utf-8") as f:
        json.dump({
            "source": source,
            "timestamp": datetime.utcnow().isoformat(),
            "items": cleaned_list
        }, f, indent=2)
    report["cleaned_files_created"] += 1

report["duplicates_removed"] = report["total_items_before"] - report["total_items_after"]

with open(LOG_FILE, "a", encoding="utf-8") as log:
    log.write(f"{datetime.utcnow().isoformat()} - Cleaned {report['files_scanned']} files, "
              f"removed {report['duplicates_removed']} duplicates, "
              f"{report['cleaned_files_created']} cleaned files created.\n")

with open(REPORT_FILE, "w", encoding="utf-8") as f:
    json.dump(report, f, indent=2)

print("✅ Cleaning complete. Summary:")
print(json.dumps(report, indent=2))

import os
import json
import glob
from datetime import datetime
from collections import defaultdict

CLEANED_DIR = "../knowledge_base/cleaned/"
DELTA_REPORT_DIR = "../knowledge_base/delta_reports/"

os.makedirs(DELTA_REPORT_DIR, exist_ok=True)

def load_json(file_path):
    try:
        with open(file_path, "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"⚠️ Failed to load {file_path}: {e}")
        return []

def extract_source(filename):
    parts = filename.split("_")
    return parts[1] if len(parts) > 1 else "unknown"

def generate_delta(old_items, new_items, key="id"):
    old_set = {json.dumps(item, sort_keys=True) for item in old_items}
    new_set = {json.dumps(item, sort_keys=True) for item in new_items}

    added = new_set - old_set
    removed = old_set - new_set

    return {
        "new_items": len(added),
        "removed_items": len(removed),
        "total_previous": len(old_items),
        "total_current": len(new_items)
    }

# 🔍 Group files by source
grouped_files = defaultdict(list)

for file in glob.glob(os.path.join(CLEANED_DIR, "*.json")):
    source = extract_source(os.path.basename(file))
    grouped_files[source].append(file)

for source, files in grouped_files.items():
    if len(files) < 2:
        print(f"⏭️ Skipping {source}, not enough files to compare.")
        continue

    # Sort by timestamp in filename
    sorted_files = sorted(files, key=lambda x: x.split("_")[-1])

    file1 = sorted_files[-2]
    file2 = sorted_files[-1]

    data1 = load_json(file1)
    data2 = load_json(file2)

    if isinstance(data1, dict):
        data1 = data1.get("articles", []) or data1.get("posts", []) or []

    if isinstance(data2, dict):
        data2 = data2.get("articles", []) or data2.get("posts", []) or []

    delta = generate_delta(data1, data2)
    delta["source"] = source
    delta["timestamp"] = datetime.utcnow().isoformat()

    filename = f"{DELTA_REPORT_DIR}delta_{source}_{datetime.utcnow().strftime('%Y%m%dT%H%M%S')}.json"
    with open(filename, "w") as f:
        json.dump(delta, f, indent=2)

    print(f"✅ Delta report saved: {filename}")

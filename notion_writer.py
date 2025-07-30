import os
from dotenv import load_dotenv
from scripts.notion_utils import (
    write_paragraph_to_notion,
    append_heading,
    append_bullet,
    read_page_blocks,
    update_paragraph,
)

load_dotenv()
page_id = os.getenv("NOTION_PAGE_ID_MASTER")  # or NOTION_PAGE_ID_KBB

print("Loaded Page ID:", page_id)

# Test writing
write_paragraph_to_notion(page_id, "✅ This paragraph was written by DataOpsGPT.")

# Test heading
append_heading(page_id, "🚀 New Section Created by Agent", level=2)

# Test bullets
append_bullet(page_id, ["• First bullet", "• Second bullet", "• Third bullet"])

# Optionally read and print all blocks
blocks = read_page_blocks(page_id)
print("🧱 Page blocks retrieved:")
for block in blocks['results']:
    print(block['id'], block['type'])
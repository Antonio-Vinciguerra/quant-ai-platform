import os
from notion_client import Client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Notion client
notion = Client(auth=os.getenv("NOTION_TOKEN"))

def write_paragraph_to_notion(page_id, text):
    response = notion.blocks.children.append(
        block_id=page_id,
        children=[
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [
                        {"type": "text", "text": {"content": text}}
                    ]
                },
            }
        ]
    )
    return response

def append_heading(page_id, text, level=2):
    heading_type = f"heading_{level}"
    response = notion.blocks.children.append(
        block_id=page_id,
        children=[
            {
                "object": "block",
                "type": heading_type,
                heading_type: {
                    "rich_text": [
                        {"type": "text", "text": {"content": text}}
                    ]
                },
            }
        ]
    )
    return response

def append_bullet(page_id, bullet_texts):
    for text in bullet_texts:
        response = notion.blocks.children.append(
            block_id=page_id,
            children=[
                {
                    "object": "block",
                    "type": "bulleted_list_item",
                    "bulleted_list_item": {
                        "rich_text": [
                            {"type": "text", "text": {"content": text}}
                        ]
                    },
                }
            ]
        )
        print("✅ Bullet added:", response)
    return True

def read_page_blocks(page_id):
    response = notion.blocks.children.list(block_id=page_id)
    return response

def update_paragraph(block_id, new_text):
    response = notion.blocks.update(
        block_id=block_id,
        paragraph={
            "rich_text": [
                {"type": "text", "text": {"content": new_text}}
            ]
        },
    )
    return response
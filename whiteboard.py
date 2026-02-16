import json
import os
from typing import Dict, List, Optional
from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field

# --- Configuration & Constraints ---
# Prevents clutter by limiting active items per section
SECTION_LIMITS = {
    "Today's Tasks": 5,      # The "3-5" Rule
    "Long-Term Goals": 3,    # Focus on a few big things
    "Project Ideas": 20,     # Storage can be larger
    "Brain Dump": 50         # The inbox
}

DB_FILE = "whiteboard_data.json"

# --- Data Models ---
class BoardItem(BaseModel):
    id: int
    content: str
    completed: bool = False
    priority: str = "Medium"  # Options: High, Medium, Low

class WhiteboardData(BaseModel):
    sections: Dict[str, List[BoardItem]] = {
        "Today's Tasks": [],
        "Long-Term Goals": [],
        "Project Ideas": [],
        "Healthy Habits": [],
        "Brain Dump": [],
        "Archive": []  # Completed items go here
    }
    next_id: int = 1

# --- Persistence ---
def load_db() -> WhiteboardData:
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f:
            data = json.load(f)
            return WhiteboardData(**data)
    return WhiteboardData()

def save_db(db: WhiteboardData):
    with open(DB_FILE, "w") as f:
        f.write(db.model_dump_json(indent=2))

# --- MCP Server ---
mcp = FastMCP("AestheticWhiteboard")

@mcp.resource("whiteboard://main")
def get_whiteboard() -> str:
    """
    Returns the live whiteboard. 
    Uses Markdown and Emojis to keep it visually scanable for Agents and Humans.
    """
    db = load_db()
    display = ["# 🖊️ TEAM PLANS & GOALS\n"]
    
    # Priority Icons
    icons = {"High": "🔥", "Medium": "🔹", "Low": "💤"}
    
    for section, items in db.sections.items():
        if section == "Archive": continue  # Hide archive to reduce context window usage
        
        # Header with capacity info
        limit = SECTION_LIMITS.get(section, "∞")
        count = len([i for i in items if not i.completed])
        display.append(f"### {section} ({count}/{limit})")
        
        if not items:
            display.append("_(Empty)_")
        
        for item in items:
            status = "✅" if item.completed else icons.get(item.priority, "🔹")
            # Strikethrough if completed
            content = f"~~{item.content}~~" if item.completed else f"**{item.content}**"
            display.append(f"- {status} {content} `[ID: {item.id}]`")
        
        display.append("")  # Spacer
        
    return "\n".join(display)

@mcp.tool()
def add_item(section: str, content: str, priority: str = "Medium") -> str:
    """
    Add a new item to a section. 
    ENFORCES LIMITS: Will fail if the section is full.
    Priorities: "High", "Medium", "Low".
    """
    db = load_db()
    
    if section not in db.sections:
        return f"Error: Section '{section}' not found. Available: {list(db.sections.keys())}"
    
    # 1. The Aesthetic Check (The "Bouncer")
    active_items = [i for i in db.sections[section] if not i.completed]
    limit = SECTION_LIMITS.get(section, 999)
    
    if len(active_items) >= limit:
        return (f"⛔ DENIED: '{section}' is full ({len(active_items)}/{limit}). "
                f"You must complete or move an item to 'Archive' or 'Brain Dump' first.")
    
    # 2. Add Item
    new_item = BoardItem(id=db.next_id, content=content, priority=priority)
    db.sections[section].append(new_item)
    db.next_id += 1
    
    save_db(db)
    return f"✨ Added '{content}' to '{section}' as {priority} priority."

@mcp.tool()
def toggle_status(item_id: int, completed: bool) -> str:
    """Mark an item as completed (True) or active (False)."""
    db = load_db()
    for section in db.sections:
        for item in db.sections[section]:
            if item.id == item_id:
                item.completed = completed
                save_db(db)
                return f"Item {item_id} marked as {'✅ Complete' if completed else 'Active'}."
    return "Item not found."

@mcp.tool()
def clean_board() -> str:
    """
    The 'Janitor' function. Moves ALL completed items to the Archive section
    to clear up visual space and slots for new tasks.
    """
    db = load_db()
    moved_count = 0
    
    for section in list(db.sections.keys()):
        if section == "Archive": continue
        
        # Separate active vs completed
        active = []
        for item in db.sections[section]:
            if item.completed:
                db.sections["Archive"].append(item)
                moved_count += 1
            else:
                active.append(item)
        
        db.sections[section] = active
        
    save_db(db)
    return f"🧹 Board Cleaned! Moved {moved_count} completed items to the Archive."

if __name__ == "__main__":
    mcp.run()

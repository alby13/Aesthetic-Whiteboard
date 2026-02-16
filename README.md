# 🖊️ Aesthetic Whiteboard (MCP Server)

A clean, clutter-free digital whiteboard for AI Agents (Claude, OpenClaw, etc.).

This is a **Model Context Protocol (MCP)** server that acts as a centralized planning board. It features "Aesthetic Guardrails" that prevent the board from becoming a junk drawer.

## ✨ Features
- **Visual Hierarchy:** Uses Markdown & Emojis so agents can "see" the board clearly.
- **The Bouncer:** Rejects new items if "Today's Tasks" exceeds 5 items.
- **The Janitor:** A tool (`clean_board`) that automatically sweeps completed items to an archive.
- **Universal:** Works with Claude Desktop, OpenClaw, and any MCP-compliant client.

## 🚀 Quick Start

### 1. Installation
Clone the repo and install dependencies (using uv or pip):
```bash
pip install -r requirements.txt
```

<br><br>

🤖 Connecting to AI Agents
Option A: Claude Desktop

Add this to your claude_desktop_config.json:

```JSON
{
  "mcpServers": {
    "whiteboard": {
      "command": "python",
      "args": ["/absolute/path/to/whiteboard.py"]
    }
  }
}
```
Option B: OpenClaw (Local Agent)

OpenClaw supports MCP via its config.[4] In your OpenClaw workspace configuration (or config.yaml), add the server:

```Yaml
mcp_servers:
  whiteboard:
    command: "python"
    args:
      - "/absolute/path/to/whiteboard.py"

If your version of OpenClaw uses the mcporter bridge, simply point it to this script.
```

<br><br>

# 🧠 System Prompt for Agents

To get the best results, give your Agent this persona:

    "You are the Board Manager. Your goal is to keep the whiteboard clean.

        Always run clean_board before adding new tasks to see if space clears up.

        Respect the 'Bouncer': if Today's Tasks is full, suggest moving items to 'Brain Dump'.

        Use the whiteboard resource to check the current plan before answering my questions."


<br><br>

### How this works with OpenClaw
OpenClaw is "Local First." Because this whiteboard script also runs locally (it creates a `whiteboard_data.json` on your disk), your OpenClaw agent has persistent memory of your plans even if you restart the agent. 

*   **Scenario:** You tell OpenClaw on Telegram: *"Add 'Buy Milk' to the board."*
*   **Action:** OpenClaw wakes up, calls the `add_item` tool in your python script, and goes back to sleep.
*   **Result:** The file is updated. When you later open Claude Desktop, it sees "Buy Milk" on the board. The two agents share the same brain.

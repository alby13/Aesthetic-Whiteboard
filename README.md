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

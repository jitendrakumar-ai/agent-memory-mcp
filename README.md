# agent# 🕸️ agent-memory-mcp

> **Persistent SQLite Knowledge Graph & Cross-Session Memory MCP Server in Python for Claude Desktop, Cursor & Autonomous AI Agents.**

---

## 🌟 Overview

`agent-memory-mcp` gives LLMs long-term episodic memory and structured knowledge graph representation across conversations. Powered by a local embedded SQLite database, it enables AI models like Claude and GPT-based agents to remember preferences, store structured facts, and link entities together over time.

---

## 🛠️ Tools Included

1. **`store_memory`**
   - Persists key-value facts and state observations into SQLite with categories and automatic ISO timestamps.
2. **`search_memories`**
   - Queries stored episodic memories using fuzzy keyword matching and category filters.
3. **`link_knowledge_entities`**
   - Creates semantic graph edges (`subject` -> `predicate` -> `object`) in SQLite to establish structured knowledge networks.
4. **`query_knowledge_graph`**
   - Traverses knowledge graph triplets to retrieve all connected concepts, entities, and context around a given target.

---

## ⚙️ MCP Installation & Setup Configs

### 1. Claude Desktop (`claude_desktop_config.json`)

Add the following to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "agent-memory-mcp": {
      "command": "python3",
      "args": [
        "/path/to/agent-memory-mcp/agent_memory_mcp.py"
      ]
    }
  }
}
```

### 2. Cursor (`.cursor/mcp.json`)

Add the following to your workspace `.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "agent-memory-mcp": {
      "command": "python3",
      "args": [
        "${workspaceFolder}/agent_memory_mcp.py"
      ]
    }
  }
}
```

---

## 🚀 Quickstart

Start the stdio MCP server directly:

```bash
python3 agent_memory_mcp.py
```

---

## 📄 License

MIT License © jitendrakumarvoicex-art (Dhruv)

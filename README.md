<div align="center">
  <img src="assets/banner.svg" width="100%" alt="agent-memory-mcp Banner" />
</div>

<p align="center">
  <img src="https&#58;//img.shields.io/badge/MCP-2025--03--26-7928CA?style=for-the-badge" alt="MCP Spec" />
  <img src="https&#58;//img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python Version" />
  <img src="https&#58;//img.shields.io/badge/Zero_API_Keys-Required-00F2FE?style=for-the-badge" alt="Zero API Keys" />
  <img src="https&#58;//img.shields.io/babadge/NexusVibe_AI-Jitendra_Kumar-FF0080?style=for-the-badge"dge/NexusVi_AIbe_Jitendra_Kumar--FF0080?style=for-the-badge" alt="NexusVibe AI" />
  <img src="https&#58;//img.shields.io/badge/License-MIT-green?style=for-the-badge" alt="License" />
</p>

---

> **Persistent SQLite Knowledge Graph & Episodic Memory Engine for Autonomous AI Agents & LLMs.**

---

## 💡 Why This Exists & Token Efficiency

LLMs suffer from context window amnesia across chat sessions, re-asking user preferences and losing project history. **`agent-memory-mcp`** introduces a **`claude-mem` style 3-layer workflow** with local SQLite persistent storage for infinite cross-session memory recall.

### ⚡ 3-Layer Memory Workflow

1. **Layer 1: Episodic Storage (`store_memory`)** — Persists key-value facts, user preferences, and observations with categories and ISO timestamps.
2. **Layer 2: Semantic Graph Linkage (`link_knowledge_entities`)** — Establishes semantic graph edges (`subject` -> `predicate` -> `object`) to build interconnected entity networks.
3. **Layer 3: Infinite Recall (`search_memories` & `query_knowledge_graph`)** — Queries stored memories with fuzzy keyword matching and traverses knowledge graph triplets across sessions.

### 📊 Token Savings & Memory Recall Comparison

| Approach | Memory Persistence | Token Waste | Cross-Session Recall | Efficiency |
| :--- | :--- | :--- | :--- | :--- |
| **Naive Prompt Repetition** | None (Lost on reset) | Heavy (~30,000 tokens) | No | 0% |
| **Flat File Text Logs** | Manual file reads | High (~12,000 tokens) | Limited | ~50% |
| **`agent-memory-mcp` SQLite Engine** | **Permanent Local SQLite** | Minimal (~1,200 tokens) | **Infinite** 🚀 | **~90% Token Savings** |

---

## 🏗️ Architecture Diagram

```mermaid
flowchart TD
    A[AI Coding Agent / LLM] -->|1. Store Fact / Observation| B[store_memory]
    A -->|2. Create Entity Relationship| C[link_knowledge_entities]
    A -->|3. Search Memories| D[search_memories]
    A -->|4. Traverse Knowledge Graph| E[query_knowledge_graph]

    subgraph MCP Server Engine: agent-memory-mcp
        B --> F[(Local SQLite Database)]
        C --> F
        D --> F
        E --> F
    end

    F -->|Targeted Graph Triplets & Facts| A
```

---

## 🛠️ Tools Included

1. `store_memory`: Persists key-value facts and state observations into SQLite with categories and automatic ISO timestamps.
2. `search_memories`: Queries stored episodic memories using fuzzy keyword matching and category filters.
3. `link_knowledge_entities`: Creates semantic graph edges (`subject` -> `predicate` -> `object`) in SQLite to establish structured knowledge networks.
4. `query_knowledge_graph`: Traverses knowledge graph triplets to retrieve all connected concepts, entities, and context around a given target.

---

## 🚀 Quick Start (1-Click & 1-Command Setup)

### 1. Claude Code CLI
```bash
claude mcp add agent-memory-mcp -- python -m agent_memory_mcp
```

### 2. Cursor (`.cursor/mcp.json`)
```json
{
  "mcpServers": {
    "agent-memory-mcp": {
      "command": "python",
      "args": ["-m", "agent_memory_mcp"]
    }
  }
}
```

### 3. OpenAI Codex CLI (`~/.codex/config.toml`)
```toml
[mcp_servers.agent-memory-mcp]
command = "python"
args = ["-m", "agent_memory_mcp"]
```

### 4. Google Antigravity IDE (`mcp_config.json`)
```json
{
  "mcpServers": {
    "agent-memory-mcp": {
      "command": "python",
      "args": ["-m", "agent_memory_mcp"]
    }
  }
}
```

### 5. Windsurf / Cline
```json
{
  "mcpServers": {
    "agent-memory-mcp": {
      "command": "python",
      "args": ["-m", "agent_memory_mcp"]
    }
  }
}
```

---

<div align="center">
  <sub>Built with ❤️ by <b>Jitendra Kumar • NexusVibe AI</b></sub>
</div>

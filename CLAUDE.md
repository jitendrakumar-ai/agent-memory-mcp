# CLAUDE.md - Developer Guide for agent-memory-mcp

## Overview
`agent-memory-mcp` is a Model Context Protocol (MCP) server that provides persistent SQLite-backed knowledge graph and cross-session memory storage for autonomous AI agents and Claude Desktop / Cursor / Codex / Antigravity / OpenCode / Windsurf IDEs.

## Quick Commands
- **Self-Test**: `python3 agent_memory_mcp.py --self-test`
- **Run Server**: `python3 agent_memory_mcp.py`
- **Docker Build**: `docker build -t agent-memory-mcp .`
- **Docker Run**: `docker run -i --rm agent-memory-mcp`

## Architecture & Code Guidelines
- Single-file stdio MCP server implementation in `agent_memory_mcp.py`.
- Zero external database dependencies; utilizes local embedded SQLite database (`memory.db`).
- Implements 3-Layer Memory System:
  1. **Episodic Memory**: Raw logs, prompt histories, temporal event timelines.
  2. **Knowledge Graph**: Entity-relation-entity triples with strict domain typing.
  3. **Work Pattern Index**: Reusable workflow heuristics, action strategies, and agent tools.

## Development Rules
- Keep zero telemetry disclosures strictly intact.
- Run `python3 agent_memory_mcp.py --self-test` before submitting any commit or PR.

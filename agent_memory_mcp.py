import sys
import json
import os
import sqlite3
from datetime import datetime

DB_FILE = os.path.expanduser("~/.agent_memory_mcp.db")

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("PRAGMA journal_mode=MEMORY;")
    cursor.execute("PRAGMA synchronous=OFF;")
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS memories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            key TEXT UNIQUE,
            value TEXT,
            category TEXT,
            timestamp TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS knowledge_graph (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            subject TEXT,
            predicate TEXT,
            object TEXT,
            timestamp TEXT,
            UNIQUE(subject, predicate, object)
        )
    ''')
    conn.commit()
    conn.close()

init_db()

def handle_request(request):
    method = request.get("method")
    req_id = request.get("id")

    if method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {"name": "agent-memory-mcp", "version": "1.0.0"}
            }
        }

    elif method == "notifications/initialized":
        return None

    elif method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "tools": [
                    {
                        "name": "store_memory",
                        "description": "Store or update a key-value memory fact in persistent SQLite store.",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "key": {"type": "string"},
                                "value": {"type": "string"},
                                "category": {"type": "string", "default": "general"}
                            },
                            "required": ["key", "value"]
                        }
                    },
                    {
                        "name": "search_memories",
                        "description": "Search stored persistent memories by keyword or category.",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "query": {"type": "string"},
                                "category": {"type": "string"}
                            }
                        }
                    },
                    {
                        "name": "link_knowledge_entities",
                        "description": "Add a entity-relationship triplet edge (subject -> predicate -> object) to knowledge graph.",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "subject": {"type": "string"},
                                "predicate": {"type": "string"},
                                "object": {"type": "string"}
                            },
                            "required": ["subject", "predicate", "object"]
                        }
                    },
                    {
                        "name": "query_knowledge_graph",
                        "description": "Query knowledge graph for connections related to a specific subject or entity.",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "entity": {"type": "string"}
                            },
                            "required": ["entity"]
                        }
                    }
                ]
            }
        }

    elif method == "tools/call":
        params = request.get("params", {})
        tool_name = params.get("name")
        args = params.get("arguments", {})

        if tool_name == "store_memory":
            res = store_memory(args.get("key"), args.get("value"), args.get("category", "general"))
        elif tool_name == "search_memories":
            res = search_memories(args.get("query"), args.get("category"))
        elif tool_name == "link_knowledge_entities":
            res = link_knowledge_entities(args.get("subject"), args.get("predicate"), args.get("object"))
        elif tool_name == "query_knowledge_graph":
            res = query_knowledge_graph(args.get("entity"))
        else:
            res = {"error": f"Unknown tool: {tool_name}"}

        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "content": [{"type": "text", "text": json.dumps(res, indent=2)}]
            }
        }

    return {
        "jsonrpc": "2.0",
        "id": req_id,
        "error": {"code": -32601, "message": "Method not found"}
    }

def store_memory(key, value, category="general"):
    if not key or not value:
        return {"error": "Both key and value are required."}
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    now = datetime.utcnow().isoformat()
    cursor.execute('''
        INSERT INTO memories (key, value, category, timestamp)
        VALUES (?, ?, ?, ?)
        ON CONFLICT(key) DO UPDATE SET value=excluded.value, category=excluded.category, timestamp=excluded.timestamp
    ''', (key, value, category, now))
    conn.commit()
    conn.close()
    return {"status": "success", "key": key, "category": category, "updated_at": now}

def search_memories(query=None, category=None):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    sql = "SELECT key, value, category, timestamp FROM memories WHERE 1=1"
    params = []
    if query:
        sql += " AND (key LIKE ? OR value LIKE ?)"
        params.extend([f"%{query}%", f"%{query}%"])
    if category:
        sql += " AND category = ?"
        params.append(category)
    cursor.execute(sql, params)
    rows = cursor.fetchall()
    conn.close()
    results = [{"key": r[0], "value": r[1], "category": r[2], "timestamp": r[3]} for r in rows]
    return {"count": len(results), "memories": results}

def link_knowledge_entities(subject, predicate, object_val):
    if not subject or not predicate or not object_val:
        return {"error": "Subject, predicate, and object are all required."}
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    now = datetime.utcnow().isoformat()
    try:
        cursor.execute('''
            INSERT INTO knowledge_graph (subject, predicate, object, timestamp)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(subject, predicate, object) DO UPDATE SET timestamp=excluded.timestamp
        ''', (subject, predicate, object_val, now))
        conn.commit()
    except Exception as e:
        conn.close()
        return {"error": str(e)}
    conn.close()
    return {"status": "linked", "triplet": {"subject": subject, "predicate": predicate, "object": object_val}}

def query_knowledge_graph(entity):
    if not entity:
        return {"error": "Entity parameter required."}
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT subject, predicate, object, timestamp FROM knowledge_graph
        WHERE subject LIKE ? OR object LIKE ?
    ''', (f"%{entity}%", f"%{entity}%"))
    rows = cursor.fetchall()
    conn.close()
    graph = [{"subject": r[0], "predicate": r[1], "object": r[2], "timestamp": r[3]} for r in rows]
    return {"entity": entity, "connected_triplets": graph}

def main():
    for line in sys.stdin:
        if not line.strip():
            continue
        try:
            req = json.loads(line)
            res = handle_request(req)
            if res:
                sys.stdout.write(json.dumps(res) + "\n")
                sys.stdout.flush()
        except Exception as e:
            err_res = {
                "jsonrpc": "2.0",
                "id": None,
                "error": {"code": -32700, "message": f"Parse error: {str(e)}"}
            }
            sys.stdout.write(json.dumps(err_res) + "\n")
            sys.stdout.flush()

if __name__ == "__main__":
    main()

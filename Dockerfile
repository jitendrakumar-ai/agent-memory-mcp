FROM python:3.11-slim

WORKDIR /app

COPY agent_memory_mcp.py .
COPY pyproject.toml .

RUN pip install --no-cache-dir mcp sqlite-utils pydantic

ENTRYPOINT ["python3", "agent_memory_mcp.py"]

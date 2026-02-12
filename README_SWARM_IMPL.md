# LifeOS Swarm Implementation Guide

This folder contains the **Reference Implementation** of the LifeOS Active Architecture.

## Directory Structure

- **`config/`**: System configuration (LLM endpoints, graph db credentials).
- **`gateway/`**: The FastAPI server acting as the Control Plane.
  - Run with: `python gateway/api_server.py`
  - Endpoints: `/ingest/context`, `/sop/upload`, `/graph/active`.
- **`brain/`**: The Core Logic.
  - `sop_engine.py`: The wrapper around LangGraph to execute Markdown SOPs.
  - `context_watcher.py`: Rule-based trigger logic (Mock).
- **`knowledge_graph/`**: Neo4j Client wrapper for strategic reasoning.
- **`knowledge/SOPs/`**: The "Cartridges" (Tactical Manuals) for the system.

## Getting Started

1. **Install Dependencies**:
   ```bash
   pip install fastapi uvicorn pydantic langgraph neo4j pyyaml
   ```

2. **Start the Brain**:
   ```bash
   python gateway/api_server.py
   ```

3. **Simulate a Trigger**:
   Use Postman or Curl to send a Context signal:
   ```bash
   curl -X POST http://localhost:8000/ingest/context \
     -H "Content-Type: application/json" \
     -d '{
       "timestamp": "2026-02-12T07:00:00Z",
       "source_device": "debug_cli",
       "context_nodes": [
         {"type": "LOCATION", "value": "Home"},
         {"type": "ACTIVITY", "value": "waking_up"}
       ]
     }'
   ```
   
   *Expected Output*: The response should contain `"triggered_sops": ["SOP_001_Morning_Briefing"]` because we defined that rule in `context_manager.py` (and theoretically in the Concept Graph).

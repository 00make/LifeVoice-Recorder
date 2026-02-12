from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Optional
import datetime

import sys
import os

# Ensure brain module is in path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from brain.context_watcher import ContextManager

app = FastAPI(title="LifeOS Gateway", version="2.0.0")

# Initialize Singletons
context_manager = ContextManager()

class ContextPayload(BaseModel):
    timestamp: str
    source_device: str
    context_nodes: List[Dict]

class SOPUploadPayload(BaseModel):
    content: str
    filename: str

@app.get("/")
def health_check():
    return {"status": "LifeOS Swarm Online", "version": "2.0.0"}

# --- Context Ingestion API ---

@app.post("/ingest/context")
def ingest_context(payload: ContextPayload):
    """
    Receives fused context data from Android/WearOS.
    Example: {"type": "LOCATION", "value": "Home"}
    """
    triggered_sops = []
    
    for Node in payload.context_nodes:
        # Standardize for ContextManager
        normalized_data = {
            "type": Node.get("type"), 
            "value": Node.get("value"),
            "metadata": Node.get("metadata", {})
        }
        
        # Ingest and check for triggers
        # Note: In real production, this should be async/queued
        potential_triggers = context_manager.ingest_sensor_data(normalized_data)
        if potential_triggers:
            triggered_sops.extend(potential_triggers)
            
    return {
        "status": "updated", 
        "current_context": context_manager.current_context,
        "triggered_sops": list(set(triggered_sops))
    }

# --- SOP Management API ---

@app.post("/sop/upload")
def upload_sop(payload: SOPUploadPayload):
    """
    Uploads a new SOP markdown file to the registry.
    """
    save_path = os.path.join("knowledge", "SOPs", payload.filename)
    try:
        with open(save_path, "w", encoding="utf-8") as f:
            f.write(payload.content)
        return {"status": "saved", "path": save_path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/graph/active")
def get_active_graph():
    """
    Mock endpoint for Visualization Layer (Commander Deck).
    """
    return {
        "nodes": [
            {"id": "ctx_home", "type": "CONTEXT", "label": "Home"},
            {"id": "sop_morning", "type": "SOP", "label": "Morning Briefing"},
            {"id": "agent_analyst", "type": "AGENT", "label": "Analyst-01", "status": "thinking"}
        ],
        "edges": [
            {"source": "ctx_home", "target": "sop_morning", "rel": "TRIGGERS"},
            {"source": "sop_morning", "target": "agent_analyst", "rel": "ASSIGNED"}
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

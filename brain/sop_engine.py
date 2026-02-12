import yaml
import re
from typing import List, Dict, Any
from pydantic import BaseModel
from langgraph.graph import StateGraph, END

class SOPStep(BaseModel):
    name: str
    role: str
    action_type: str
    instruction: str
    next_steps: List[str] = []

class SOP(BaseModel):
    id: str
    triggers: List[Dict]
    roles: List[Dict]
    steps: List[SOPStep]

class AgentState(BaseModel):
    """The State passed between nodes in the LangGraph"""
    context: Dict[str, Any]
    history: List[str]
    current_step_output: Any = None
    errors: List[str] = []

class SOPEngine:
    def __init__(self, sop_file_path: str):
        self.sop = self._parse_sop_md(sop_file_path)
        self.workflow = self._build_graph()

    def _parse_sop_md(self, path: str) -> SOP:
        """
        Parses the Markdown file with Frontmatter + regex for Steps.
        (Simplified implementation for demo purposes)
        """
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 1. Extract YAML Frontmatter
        parts = content.split('---')
        metadata = yaml.safe_load(parts[1])
        body = parts[2]

        # 2. Extract Steps (Regex looking for ## Step X: Name)
        steps = []
        # Regex to find sections like "## Step 1: name ... ## Step 2:"
        # For this demo, let's assume a simplified list
        # detailed parsing logic would go here.
        
        # Mocking parsing result for SOP_001
        if "Morning" in metadata['id']:
             steps = [
                SOPStep(name="step_1", role="analyst", action_type="ToolCall", instruction="Gather data...", next_steps=["step_2"]),
                SOPStep(name="step_2", role="analyst", action_type="Analysis", instruction="Analyze...", next_steps=["step_3"]),
                SOPStep(name="step_3", role="writer", action_type="Draft", instruction="Write briefing...", next_steps=["end"])
             ]
        
        return SOP(
            id=metadata['id'], 
            triggers=metadata.get('triggers', []), 
            roles=metadata.get('roles', []), 
            steps=steps
        )

    def _create_node_function(self, step: SOPStep):
        """Factory that creates the Python function for a Graph Node"""
        def node_fn(state: AgentState):
            print(f"[{step.role.upper()}] Executing {step.name}...")
            # In real life: call LLM / Tool here
            # result = llm.invoke(step.instruction, context=state.context)
            
            # Simulate output
            output = f"Output form {step.name}"
            state.history.append(f"{step.name}: {output}")
            state.current_step_output = output
            return state
        return node_fn

    def _build_graph(self):
        workflow = StateGraph(AgentState)
        
        # 1. Add Nodes
        for step in self.sop.steps:
            workflow.add_node(step.name, self._create_node_function(step))
            
        # 2. Add Edges
        workflow.set_entry_point(self.sop.steps[0].name)
        
        for step in self.sop.steps:
            for next_step_name in step.next_steps:
                if next_step_name == "end":
                    workflow.add_edge(step.name, END)
                else:
                    workflow.add_edge(step.name, next_step_name)
                    
        return workflow.compile()

    def run(self, initial_context: Dict):
        print(f"🚀 Starting SOP: {self.sop.id}")
        app = self.workflow
        initial_state = AgentState(context=initial_context, history=[])
        result = app.invoke(initial_state)
        print("✅ SOP Execution Finished")
        return result

# Example Usage
if __name__ == "__main__":
    engine = SOPEngine("c:/GitHub/LifeVoice-Recorder/knowledge/SOPs/SOP_001_Morning_Briefing.md")
    final_state = engine.run({"time": "07:00", "location": "Home"})
    print(final_state)

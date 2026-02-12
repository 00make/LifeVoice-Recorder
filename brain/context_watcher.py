from typing import List, Dict
import datetime

class ContextManager:
    """
    LifeOS Context Awareness Node.
    负责接收 Sensor 数据、维护 Context Graph 状态，并触发 SOP。
    """
    
    def __init__(self):
        self.current_context = {
            "location": "unknown",
            "activity": "unknown",
            "energy": 50, # 0-100
            "connected_devices": []
        }
        self.sop_triggers = [
            {
                "sop_id": "SOP_001_Morning_Briefing", 
                "condition": lambda ctx: ctx['activity'] == 'waking_up' and ctx['location'] == 'home'
            },
            {
                "sop_id": "SOP_deep_work_guard", 
                "condition": lambda ctx: ctx['location'] == 'office' and ctx['noise_level'] < 40
            }
        ]

    def ingest_sensor_data(self, payload: Dict):
        """
        Receives data from Android / Wear OS API.
        Payload e.g.: {"source": "pixel", "type": "ACTIVITY", "value": "waking_up"}
        """
        key_map = {
            "LOCATION": "location",
            "ACTIVITY": "activity",
            "BIO_ENERGY": "energy",
            "ENV_NOISE": "noise_level"
        }
        
        data_type = payload.get("type")
        value = payload.get("value")
        
        if data_type in key_map:
            target_key = key_map[data_type]
            print(f"[Context] Updating {target_key}: {self.current_context.get(target_key)} -> {value}")
            self.current_context[target_key] = value
            
            # After update, check triggers
            self._evaluate_triggers()

    def _evaluate_triggers(self):
        """
        Checks if current context matches any SOP trigger conditions.
        """
        print(f"[Context] Evaluating Triggers against: {self.current_context}...")
        
        active_sops = []
        for trigger in self.sop_triggers:
            try:
                if trigger['condition'](self.current_context):
                    print(f"⚡ TRIGGER MATCHED: {trigger['sop_id']}")
                    active_sops.append(trigger['sop_id'])
                    # Here we would call the Orchestrator
                    # orchestrator.run(trigger['sop_id'])
            except KeyError:
                continue # context not fully populated yet
                
        return active_sops

# Example Usage
if __name__ == "__main__":
    cm = ContextManager()
    
    # Simulate waking up
    cm.ingest_sensor_data({"type": "LOCATION", "value": "home"})
    cm.ingest_sensor_data({"type": "ACTIVITY", "value": "waking_up"}) 
    # Output should show Update logs and Trigger match

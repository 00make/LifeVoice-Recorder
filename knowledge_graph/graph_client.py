from neo4j import GraphDatabase
import os
import yaml

class KnowledgeGraphClient:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def register_context_node(self, context_type, value):
        """Creates or updates a Context node."""
        with self.driver.session() as session:
            session.run("""
                MERGE (c:Context {type: $type, value: $value})
                ON CREATE SET c.created_at = timestamp()
                ON MATCH SET c.last_seen = timestamp()
            """, type=context_type, value=value)

    def link_trigger(self, context_type, context_value, sop_id, probability=1.0):
        """Links a Context to an SOP with a TRIGGERS relationship."""
        with self.driver.session() as session:
            session.run("""
                MATCH (c:Context {type: $type, value: $value})
                MERGE (s:SOP {id: $sop_id})
                MERGE (c)-[r:TRIGGERS]->(s)
                SET r.probability = $prob
            """, type=context_type, value=context_value, sop_id=sop_id, prob=probability)

    def find_triggered_sops(self, context_map):
        """
        Query the grah to find SOPs triggered by current context state.
        context_map: e.g. {'LOCATION': 'Home', 'ACTIVITY': 'Waking Up'}
        """
        triggered = []
        with self.driver.session() as session:
            # Simplified query logic
            for c_type, c_value in context_map.items():
                result = session.run("""
                    MATCH (c:Context {type: $type, value: $value})-[r:TRIGGERS]->(s:SOP)
                    WHERE r.probability > 0.8
                    RETURN s.id as sop_id
                """, type=c_type, value=c_value)
                for record in result:
                    triggered.append(record["sop_id"])
        return list(set(triggered))

# Helper to init from config
def get_graph_client():
    # In real world, load from config.yaml
    uri = "bolt://localhost:7687"
    user = "neo4j"
    password = os.getenv("NEO4J_PASSWORD", "password")
    return KnowledgeGraphClient(uri, user, password)

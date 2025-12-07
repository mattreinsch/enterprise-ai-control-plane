from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class ControlPlaneAgent:
    """
    Base abstraction for any agent the Control Plane can call.

    This might wrap:
    - A Snowflake Intelligence Agent
    - A governance evaluation agent
    - An Atlas-triggering agent
    """

    name: str
    description: str

    def run(self, **kwargs) -> Dict[str, Any]:
        raise NotImplementedError("Agent.run must be implemented by subclasses.")


@dataclass
class IntelligenceAgent(ControlPlaneAgent):
    session: Any  # Snowflake Snowpark session
    agent_impl: Any  # e.g., snowflake-intelligence-agent-v2.IntelligenceAgent

    def run(self, query: str, **kwargs) -> Dict[str, Any]:
        result = self.agent_impl.run(query=query)
        return {
            "agent": self.name,
            "query": query,
            "result": result,
        }


@dataclass
class AtlasAgent(ControlPlaneAgent):
    session: Any  # Snowflake Snowpark session

    def run(self, action: str, **kwargs) -> Dict[str, Any]:
        """
        Thin abstraction to call Atlas-related stored procedures or tasks.

        e.g., action = "check_drift", "trigger_retrain"
        """
        if action == "check_drift":
            sql = "CALL ATLAS_PLATFORM_DB.ATLAS_MONITORING.CHECK_DRIFT();"
        elif action == "trigger_retrain":
            sql = "CALL ATLAS_PLATFORM_DB.ATLAS_MONITORING.TRIGGER_RETRAIN();"
        else:
            return {"error": f"Unknown Atlas action: {action}"}

        df = self.session.sql(sql).collect()
        return {
            "agent": self.name,
            "action": action,
            "result": [row.as_dict() for row in df],
        }

from dataclasses import dataclass, field
from typing import Dict, Callable, Any, Optional


@dataclass
class RegisteredAgent:
    name: str
    description: str
    handler: Callable[..., Any]


@dataclass
class RegisteredWorkflow:
    name: str
    description: str
    entrypoint: Callable[..., Any]


@dataclass
class ControlPlaneRegistry:
    """
    In-memory registry for agents and workflows.

    In a production system, this could be backed by a Snowflake table
    or a metadata service. For V1, in-memory is enough to show the pattern.
    """
    agents: Dict[str, RegisteredAgent] = field(default_factory=dict)
    workflows: Dict[str, RegisteredWorkflow] = field(default_factory=dict)

    def register_agent(
        self,
        name: str,
        description: str,
        handler: Callable[..., Any]
    ) -> None:
        self.agents[name] = RegisteredAgent(
            name=name,
            description=description,
            handler=handler,
        )

    def get_agent(self, name: str) -> Optional[RegisteredAgent]:
        return self.agents.get(name)

    def register_workflow(
        self,
        name: str,
        description: str,
        entrypoint: Callable[..., Any]
    ) -> None:
        self.workflows[name] = RegisteredWorkflow(
            name=name,
            description=description,
            entrypoint=entrypoint,
        )

    def get_workflow(self, name: str) -> Optional[RegisteredWorkflow]:
        return self.workflows.get(name)

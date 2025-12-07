from dataclasses import dataclass
from typing import Dict, Any, Callable, List

from .observability import RunLogger
from .policies import PolicyEngine
from .utils import generate_run_id


@dataclass
class Workflow:
    """
    A Workflow defines a high-level orchestration pattern.

    Example:
        - Atlas checks drift
        - Policy engine decides whether to act
        - If yes: trigger retraining + call Intelligence Agent + notify Slack
    """
    name: str
    description: str
    handler: Callable[..., Dict[str, Any]]


class WorkflowEngine:
    """
    Executes workflows and logs their runs.
    """

    def __init__(
        self,
        logger: RunLogger,
        policy_engine: PolicyEngine,
    ):
        self.logger = logger
        self.policy_engine = policy_engine
        self.workflows: Dict[str, Workflow] = {}

    def register_workflow(
        self,
        name: str,
        description: str,
        handler: Callable[..., Dict[str, Any]]
    ) -> None:
        self.workflows[name] = Workflow(
            name=name,
            description=description,
            handler=handler,
        )

    def run_workflow(
        self,
        name: str,
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        workflow = self.workflows.get(name)
        if not workflow:
            raise ValueError(f"Unknown workflow: {name}")

        run_id = generate_run_id(prefix=name)
        self.logger.log_start(run_id, name, context)

        try:
            result = workflow.handler(
                context=context,
                policy_engine=self.policy_engine,
                logger=self.logger,
                run_id=run_id,
            )
            self.logger.log_success(run_id, result)
            return {
                "run_id": run_id,
                "workflow": name,
                "status": "SUCCESS",
                "result": result,
            }
        except Exception as exc:
            self.logger.log_failure(run_id, exc)
            return {
                "run_id": run_id,
                "workflow": name,
                "status": "FAILED",
                "error": str(exc),
            }

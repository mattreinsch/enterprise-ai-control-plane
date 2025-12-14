import uuid
from datetime import datetime
from typing import Dict, Any

from .models import Workflow, RunLog, Policy
from .policy_engine import PolicyEngine
from .run_log import RunLogWriter

class WorkflowEngine:
    """
    Orchestrates the execution of workflows, including policy evaluation and logging.
    """

    def __init__(self, policy_engine: PolicyEngine, run_log_writer: RunLogWriter, policy_registry: Dict[str, Policy]):
        """
        Initializes the workflow engine.

        Args:
            policy_engine: An instance of the PolicyEngine.
            run_log_writer: An instance of the RunLogWriter.
            policy_registry: A dictionary mapping policy_ids to Policy objects.
        """
        self.policy_engine = policy_engine
        self.run_log_writer = run_log_writer
        self.policy_registry = policy_registry

    def run(self, workflow: Workflow, trigger_data: Dict[str, Any]):
        """
        Executes a workflow from detection to recording.

        Args:
            workflow: The Workflow to execute.
            trigger_data: The data that triggered the workflow.
        """
        run_id = str(uuid.uuid4())
        run_log = RunLog(
            run_id=run_id,
            workflow_name=workflow.name,
            status="started",
            start_time=datetime.utcnow(),
            input_data=trigger_data
        )

        try:
            # 1. Detect (assumed to have happened to trigger this run)
            print(f"INFO: Workflow '{workflow.name}' triggered for run_id: {run_id}")

            # 2. Evaluate Policies
            decisions = self._evaluate_policies(workflow, trigger_data)
            run_log.decisions = decisions

            # Check for any 'deny' decisions
            if any(d.decision == 'deny' for d in decisions):
                raise PermissionError("Workflow execution denied by policy.")

            # 3. Orchestrate Actions
            self._orchestrate_actions(workflow)

            # 4. Record final status
            run_log.status = "completed"

        except Exception as e:
            print(f"ERROR: Workflow '{workflow.name}' failed: {e}")
            run_log.status = "failed"
            run_log.errors.append(str(e))

        finally:
            run_log.end_time = datetime.utcnow()
            self.run_log_writer.write_log(run_log)
            print(f"INFO: Workflow '{workflow.name}' finished with status: {run_log.status}")

    def _evaluate_policies(self, workflow: Workflow, data: Dict[str, Any]):
        """Stub for policy evaluation step."""
        print("INFO: Evaluating policies...")
        decisions = []
        for policy_id in workflow.policies:
            policy = self.policy_registry.get(policy_id)
            if not policy:
                raise ValueError(f"Policy '{policy_id}' not found in registry.")
            
            decision = self.policy_engine.evaluate(policy, data)
            decisions.append(decision)
        return decisions

    def _orchestrate_actions(self, workflow: Workflow):
        """Stub for the orchestration step."""
        print("INFO: Orchestrating actions...")
        for step in workflow.steps:
            print(f"  - Executing step: {step['name']} (type: {step['type']})")
            # In a real engine, this would call connectors or other services.
        print("INFO: Action orchestration complete.")


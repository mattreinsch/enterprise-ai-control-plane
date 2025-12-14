from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, Any, List

@dataclass
class Policy:
    """Represents a single policy to be evaluated."""
    policy_id: str
    name: str
    description: str
    rules: List[Dict[str, Any]]
    created_at: datetime = field(default_factory=datetime.utcnow)

@dataclass
class Decision:
    """Represents the outcome of a policy evaluation."""
    policy_id: str
    decision: str  # e.g., "allow", "deny", "needs_review"
    details: Dict[str, Any]
    timestamp: datetime = field(default_factory=datetime.utcnow)

@dataclass
class RunLog:
    """Represents a log entry for a workflow run."""
    run_id: str
    workflow_name: str
    status: str  # e.g., "started", "completed", "failed"
    start_time: datetime
    end_time: datetime = None
    input_data: Dict[str, Any] = field(default_factory=dict)
    decisions: List[Decision] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)

@dataclass
class Workflow:
    """Represents a workflow to be executed by the control plane."""
    workflow_id: str
    name: str
    description: str
    steps: List[Dict[str, Any]]
    policies: List[str]  # List of policy_ids to evaluate
    created_at: datetime = field(default_factory=datetime.utcnow)

from dataclasses import dataclass
from typing import Dict, Any, Optional, List


@dataclass
class Policy:
    """
    Simple representation of a policy in the Control Plane.

    This can represent:
    - drift thresholds
    - governance constraints (e.g., no PII to external tools)
    - risk levels and escalation rules
    """
    name: str
    description: str
    conditions: Dict[str, Any]  # e.g., {"max_drift": 0.15}
    actions: List[str]          # e.g., ["trigger_retrain", "notify_security"]


class PolicyEngine:
    """
    Central policy interpretation layer.

    V1 keeps evaluation logic simple and transparent.
    """

    def __init__(self, policies: Dict[str, Policy]):
        self._policies = policies

    def get_policy(self, name: str) -> Optional[Policy]:
        return self._policies.get(name)

    def evaluate(
        self,
        policy_name: str,
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Evaluate a policy given a context.

        Returns:
            {
                "policy": <Policy or None>,
                "should_act": bool,
                "actions": [...],
                "reason": str
            }
        """
        policy = self._policies.get(policy_name)
        if not policy:
            return {
                "policy": None,
                "should_act": False,
                "actions": [],
                "reason": f"No policy named {policy_name}."
            }

        # Example: drift policy
        max_drift = policy.conditions.get("max_drift")
        observed_drift = context.get("observed_drift")

        if max_drift is not None and observed_drift is not None:
            if observed_drift > max_drift:
                return {
                    "policy": policy,
                    "should_act": True,
                    "actions": policy.actions,
                    "reason": (
                        f"Observed drift {observed_drift} exceeds "
                        f"threshold {max_drift}."
                    ),
                }
            else:
                return {
                    "policy": policy,
                    "should_act": False,
                    "actions": [],
                    "reason": (
                        f"Observed drift {observed_drift} is within "
                        f"threshold {max_drift}."
                    ),
                }

        # Default: no decision
        return {
            "policy": policy,
            "should_act": False,
            "actions": [],
            "reason": "No applicable evaluation rule for this policy/context.",
        }

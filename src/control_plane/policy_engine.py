from typing import Dict, Any
from .models import Policy, Decision

class PolicyEngine:
    """
    Evaluates policies against provided data to make decisions.
    """

    def evaluate(self, policy: Policy, data: Dict[str, Any]) -> Decision:
        """
        Evaluates a single policy based on the input data.

        This is a stub implementation. A real policy engine would parse
        the policy's rules and evaluate them against the data.

        Args:
            policy: The Policy object to evaluate.
            data: The data to evaluate the policy against.

        Returns:
            A Decision object representing the outcome.
        """
        print(f"INFO: Evaluating policy: {policy.name} ({policy.policy_id})")

        # Stub logic: For demonstration, we'll just assume the policy
        # passes if the input data contains a 'user_role' of 'admin'.
        is_allowed = data.get("user_role") == "admin"
        decision_str = "allow" if is_allowed else "deny"

        decision = Decision(
            policy_id=policy.policy_id,
            decision=decision_str,
            details={
                "message": f"Decision '{decision_str}' based on stub logic.",
                "evaluated_rules": policy.rules
            }
        )

        print(f"INFO: Policy decision: {decision.decision}")
        return decision

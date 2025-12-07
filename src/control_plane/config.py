from dataclasses import dataclass
from typing import Optional


@dataclass
class ControlPlaneConfig:
    """
    Global configuration object for the Control Plane.

    In a real deployment, this would likely be populated from:
    - environment variables
    - a configuration table in Snowflake
    - secrets managers (for webhooks, etc.)
    """
    environment: str = "dev"
    run_log_table: str = "CONTROL_PLANE_DB.CONTROL_PLANE_MONITORING.RUN_LOG"
    default_timezone: str = "UTC"
    enable_external_actions: bool = False
    slack_webhook_secret_name: Optional[str] = None

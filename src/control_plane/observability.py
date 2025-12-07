from dataclasses import dataclass
from typing import Any, Dict
from datetime import datetime


@dataclass
class RunLogger:
    """
    Simple run logger.

    V1 prints to stdout and optionally writes to a Snowflake table if
    a Snowpark session is provided.
    """

    session: Any  # Snowpark session or None
    run_log_table: str

    def _now(self) -> str:
        return datetime.utcnow().isoformat()

    def log_start(self, run_id: str, workflow: str, context: Dict[str, Any]) -> None:
        print(f"[{self._now()}] START {workflow} run_id={run_id} context={context}")
        if self.session:
            self.session.sql(
                f"""
                INSERT INTO {self.run_log_table} (RUN_ID, WORKFLOW, STATUS, DETAILS, CREATED_AT)
                SELECT '{run_id}', '{workflow}', 'START', PARSE_JSON('{str(context)}'), CURRENT_TIMESTAMP();
                """
            ).collect()

    def log_success(self, run_id: str, result: Dict[str, Any]) -> None:
        print(f"[{self._now()}] SUCCESS run_id={run_id} result={result}")
        if self.session:
            self.session.sql(
                f"""
                UPDATE {self.run_log_table}
                SET STATUS = 'SUCCESS',
                    DETAILS = PARSE_JSON('{str(result)}'),
                    UPDATED_AT = CURRENT_TIMESTAMP()
                WHERE RUN_ID = '{run_id}';
                """
            ).collect()

    def log_failure(self, run_id: str, exc: Exception) -> None:
        print(f"[{self._now()}] FAILURE run_id={run_id} error={exc}")
        if self.session:
            self.session.sql(
                f"""
                UPDATE {self.run_log_table}
                SET STATUS = 'FAILED',
                    DETAILS = PARSE_JSON('{{"error": "{str(exc)}"}}'),
                    UPDATED_AT = CURRENT_TIMESTAMP()
                WHERE RUN_ID = '{run_id}';
                """
            ).collect()

import json
import logging
from datetime import datetime, timezone


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

handler = logging.StreamHandler()
handler.setLevel(logging.INFO)
logger.addHandler(handler)


def log_action(
    project_id: str,
    action: str,
    cost_amount: float,
    budget_amount: float,
    scope: str,
    message: str = "",
) -> None:
    """Log a billing action as structured JSON."""
    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "project_id": project_id,
        "action": action,
        "cost_amount": cost_amount,
        "budget_amount": budget_amount,
        "scope": scope,
        "message": message,
    }
    logger.info(json.dumps(entry))

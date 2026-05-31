import json
import logging
from datetime import datetime, timezone


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

handler = logging.StreamHandler()
handler.setLevel(logging.INFO)
logger.addHandler(handler)


def log_action(project_id: str, action: str, message: str = "") -> None:
    """Log a billing action as structured JSON."""
    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "project_id": project_id,
        "action": action,
        "message": message,
    }
    logger.info(json.dumps(entry))


def log_summary(total: int, enabled: int, skipped: int, errors: int) -> None:
    """Log the re-enable summary as structured JSON."""
    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "action": "reenable_summary",
        "total": total,
        "enabled": enabled,
        "skipped": skipped,
        "errors": errors,
    }
    logger.info(json.dumps(entry))

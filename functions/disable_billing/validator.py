from typing import Literal


def validate_payload(data: dict) -> tuple[bool, str]:
    """Validate that the Pub/Sub payload contains required fields."""
    if "costAmount" not in data:
        return False, "Missing required field: costAmount"
    if "budgetAmount" not in data:
        return False, "Missing required field: budgetAmount"
    return True, ""


def check_threshold(data: dict) -> bool:
    """Check if cost has reached or exceeded 100% of budget."""
    cost = data["costAmount"]
    budget = data["budgetAmount"]
    if budget == 0:
        return False
    return cost / budget >= 1.0


def detect_scope(data: dict) -> Literal["project", "account"]:
    """Detect whether the alert is project-level or account-level."""
    if "projectId" in data and data["projectId"]:
        return "project"
    return "account"

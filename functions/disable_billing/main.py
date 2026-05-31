import base64
import json

import functions_framework

from validator import validate_payload, check_threshold, detect_scope
from project_loader import load_projects, get_billing_account_id
from billing_service import get_billing_status, disable_billing
from notifier import notify_billing_disabled_summary
from logger import log_action


@functions_framework.cloud_event
def disable_billing_handler(cloud_event):
    """Cloud Function entry point — Pub/Sub trigger.

    Disables billing when budget threshold is reached.
    Never raises exceptions to prevent Pub/Sub retry loops.
    """
    try:
        # Decode Pub/Sub message
        raw_data = base64.b64decode(cloud_event.data["message"]["data"])
        data = json.loads(raw_data)

        # Validate payload
        valid, reason = validate_payload(data)
        if not valid:
            log_action(
                project_id="",
                action="skipped",
                cost_amount=0,
                budget_amount=0,
                scope="unknown",
                message=f"Invalid payload: {reason}",
            )
            return

        # Check threshold
        if not check_threshold(data):
            log_action(
                project_id="",
                action="skipped",
                cost_amount=data["costAmount"],
                budget_amount=data["budgetAmount"],
                scope="unknown",
                message="Below 100% threshold, no action taken",
            )
            return

        # Determine scope
        scope = detect_scope(data)
        cost_amount = data["costAmount"]
        budget_amount = data["budgetAmount"]

        # Get target projects
        if scope == "project":
            project_ids = [data["projectId"]]
        else:
            projects = load_projects()
            project_ids = [p["project_id"] for p in projects]

        billing_account_id = get_billing_account_id()

        # Disable billing on each project
        disabled_projects = []
        for project_id in project_ids:
            status = get_billing_status(project_id, billing_account_id)
            if status:
                result = disable_billing(project_id)
                if result:
                    disabled_projects.append(project_id)
                    log_action(
                        project_id=project_id,
                        action="disabled",
                        cost_amount=cost_amount,
                        budget_amount=budget_amount,
                        scope=scope,
                        message="Billing disabled successfully",
                    )
                else:
                    log_action(
                        project_id=project_id,
                        action="error",
                        cost_amount=cost_amount,
                        budget_amount=budget_amount,
                        scope=scope,
                        message="Failed to disable billing",
                    )
            else:
                log_action(
                    project_id=project_id,
                    action="already_disabled",
                    cost_amount=cost_amount,
                    budget_amount=budget_amount,
                    scope=scope,
                    message="Already disabled, skip",
                )

        # Send Telegram notification
        if disabled_projects:
            notify_billing_disabled_summary(
                disabled_projects, cost_amount, budget_amount, scope
            )

    except Exception as e:
        # Never raise — prevent Pub/Sub retry loop
        log_action(
            project_id="",
            action="error",
            cost_amount=0,
            budget_amount=0,
            scope="unknown",
            message=f"Unhandled error: {str(e)}",
        )

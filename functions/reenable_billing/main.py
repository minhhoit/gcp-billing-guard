import functions_framework
from flask import jsonify

from project_loader import load_projects, get_billing_account_id
from billing_service import get_billing_status, enable_billing
from logger import log_action, log_summary


@functions_framework.http
def reenable_billing(request):
    """Cloud Function entry point — HTTP trigger.

    Re-enables billing on all managed projects that are currently disabled.
    Always returns HTTP 200 with a JSON summary.
    """
    projects = load_projects()
    billing_account_id = get_billing_account_id()

    enabled = 0
    skipped = 0
    errors = 0

    for project in projects:
        project_id = project["project_id"]
        status = get_billing_status(project_id, billing_account_id)

        if status:
            log_action(
                project_id=project_id,
                action="skipped",
                message="Billing already active, skip",
            )
            skipped += 1
        else:
            result = enable_billing(project_id, billing_account_id)
            if result:
                log_action(
                    project_id=project_id,
                    action="enabled",
                    message="Billing re-enabled successfully",
                )
                enabled += 1
            else:
                log_action(
                    project_id=project_id,
                    action="error",
                    message="Failed to re-enable billing",
                )
                errors += 1

    total = len(projects)
    log_summary(total=total, enabled=enabled, skipped=skipped, errors=errors)

    return jsonify({
        "total": total,
        "enabled": enabled,
        "skipped": skipped,
        "errors": errors,
    }), 200

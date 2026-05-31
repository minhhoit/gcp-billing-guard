import logging

from googleapiclient import discovery
from google.auth import default

logger = logging.getLogger(__name__)


def _get_billing_client():
    """Build the Cloud Billing API client."""
    credentials, _ = default()
    return discovery.build("cloudbilling", "v1", credentials=credentials)


def get_billing_status(project_id: str, billing_account_id: str = "") -> bool:
    """Check if billing is enabled for a project.

    Uses billingAccounts.projects.list to check status via billing account
    permissions (avoids needing project-level IAM).
    """
    try:
        if not billing_account_id:
            return False
        client = _get_billing_client()
        billing_name = f"billingAccounts/{billing_account_id}"
        request = client.billingAccounts().projects().list(name=billing_name)
        while request is not None:
            response = request.execute()
            for info in response.get("projectBillingInfo", []):
                if info.get("projectId") == project_id:
                    return info.get("billingEnabled", False)
            request = client.billingAccounts().projects().list_next(
                previous_request=request, previous_response=response
            )
        return False
    except Exception as e:
        logger.error(f"Error getting billing status for {project_id}: {e}")
        return False


def enable_billing(project_id: str, billing_account_id: str) -> bool:
    """Enable billing for a project by linking it to a billing account."""
    try:
        client = _get_billing_client()
        client.projects().updateBillingInfo(
            name=f"projects/{project_id}",
            body={"billingAccountName": f"billingAccounts/{billing_account_id}"},
        ).execute()
        return True
    except Exception as e:
        logger.error(f"Error enabling billing for {project_id}: {e}")
        return False

import sys
import os
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../functions/disable_billing"))

from billing_service import get_billing_status, disable_billing

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../functions/reenable_billing"))

from billing_service import enable_billing


class TestGetBillingStatus:
    @patch("billing_service._get_billing_client")
    def test_billing_enabled(self, mock_client):
        mock_projects = MagicMock()
        mock_projects.getBillingInfo.return_value.execute.return_value = {
            "billingEnabled": True
        }
        mock_client.return_value.projects.return_value = mock_projects

        result = get_billing_status("test-project")
        assert result is True

    @patch("billing_service._get_billing_client")
    def test_billing_disabled(self, mock_client):
        mock_projects = MagicMock()
        mock_projects.getBillingInfo.return_value.execute.return_value = {
            "billingEnabled": False
        }
        mock_client.return_value.projects.return_value = mock_projects

        result = get_billing_status("test-project")
        assert result is False

    @patch("billing_service._get_billing_client")
    def test_api_error_returns_false(self, mock_client):
        mock_client.side_effect = Exception("API Error")

        result = get_billing_status("test-project")
        assert result is False


class TestDisableBilling:
    @patch("billing_service._get_billing_client")
    def test_successful_disable(self, mock_client):
        mock_projects = MagicMock()
        mock_projects.updateBillingInfo.return_value.execute.return_value = {}
        mock_client.return_value.projects.return_value = mock_projects

        result = disable_billing("test-project")
        assert result is True

    @patch("billing_service._get_billing_client")
    def test_failed_disable(self, mock_client):
        mock_projects = MagicMock()
        mock_projects.updateBillingInfo.return_value.execute.side_effect = Exception("Error")
        mock_client.return_value.projects.return_value = mock_projects

        result = disable_billing("test-project")
        assert result is False


class TestEnableBilling:
    @patch("billing_service._get_billing_client")
    def test_successful_enable(self, mock_client):
        mock_projects = MagicMock()
        mock_projects.updateBillingInfo.return_value.execute.return_value = {}
        mock_client.return_value.projects.return_value = mock_projects

        result = enable_billing("test-project", "012345-6789AB-CDEF01")
        assert result is True

    @patch("billing_service._get_billing_client")
    def test_failed_enable(self, mock_client):
        mock_projects = MagicMock()
        mock_projects.updateBillingInfo.return_value.execute.side_effect = Exception("Error")
        mock_client.return_value.projects.return_value = mock_projects

        result = enable_billing("test-project", "012345-6789AB-CDEF01")
        assert result is False

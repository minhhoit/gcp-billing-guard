import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../functions/disable_billing"))

from validator import validate_payload, check_threshold, detect_scope


class TestValidatePayload:
    def test_valid_payload(self):
        data = {"costAmount": 1000, "budgetAmount": 1000}
        valid, reason = validate_payload(data)
        assert valid is True
        assert reason == ""

    def test_missing_cost_amount(self):
        data = {"budgetAmount": 1000}
        valid, reason = validate_payload(data)
        assert valid is False
        assert "costAmount" in reason

    def test_missing_budget_amount(self):
        data = {"costAmount": 1000}
        valid, reason = validate_payload(data)
        assert valid is False
        assert "budgetAmount" in reason

    def test_empty_payload(self):
        data = {}
        valid, reason = validate_payload(data)
        assert valid is False


class TestCheckThreshold:
    def test_at_100_percent(self):
        data = {"costAmount": 1000, "budgetAmount": 1000}
        assert check_threshold(data) is True

    def test_above_100_percent(self):
        data = {"costAmount": 1500, "budgetAmount": 1000}
        assert check_threshold(data) is True

    def test_below_100_percent(self):
        data = {"costAmount": 800, "budgetAmount": 1000}
        assert check_threshold(data) is False

    def test_zero_budget(self):
        data = {"costAmount": 100, "budgetAmount": 0}
        assert check_threshold(data) is False

    def test_exactly_at_boundary(self):
        data = {"costAmount": 999999, "budgetAmount": 1000000}
        assert check_threshold(data) is False


class TestDetectScope:
    def test_project_scope(self):
        data = {"projectId": "my-project", "costAmount": 100, "budgetAmount": 100}
        assert detect_scope(data) == "project"

    def test_account_scope_no_field(self):
        data = {"costAmount": 100, "budgetAmount": 100}
        assert detect_scope(data) == "account"

    def test_account_scope_empty_string(self):
        data = {"projectId": "", "costAmount": 100, "budgetAmount": 100}
        assert detect_scope(data) == "account"

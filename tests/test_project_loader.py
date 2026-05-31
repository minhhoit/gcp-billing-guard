import sys
import os
import json
import tempfile

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../functions/disable_billing"))


class TestProjectLoader:
    def test_load_projects_success(self):
        config = {
            "billing_account_id": "012345-6789AB-CDEF01",
            "projects": [
                {"project_id": "proj-1", "display_name": "Project 1"},
                {"project_id": "proj-2", "display_name": "Project 2"},
            ],
        }
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump(config, f)
            config_path = f.name

        try:
            os.environ["CONFIG_PATH"] = config_path
            # Re-import to pick up new env var
            import importlib
            import project_loader
            importlib.reload(project_loader)

            projects = project_loader.load_projects()
            assert len(projects) == 2
            assert projects[0]["project_id"] == "proj-1"
        finally:
            os.unlink(config_path)
            del os.environ["CONFIG_PATH"]

    def test_load_projects_file_not_found(self):
        os.environ["CONFIG_PATH"] = "/nonexistent/path.json"
        import importlib
        import project_loader
        importlib.reload(project_loader)

        projects = project_loader.load_projects()
        assert projects == []
        del os.environ["CONFIG_PATH"]

    def test_load_projects_invalid_json(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            f.write("not valid json{{{")
            config_path = f.name

        try:
            os.environ["CONFIG_PATH"] = config_path
            import importlib
            import project_loader
            importlib.reload(project_loader)

            projects = project_loader.load_projects()
            assert projects == []
        finally:
            os.unlink(config_path)
            del os.environ["CONFIG_PATH"]

    def test_get_billing_account_id(self):
        config = {
            "billing_account_id": "AABBCC-DDEEFF-001122",
            "projects": [],
        }
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump(config, f)
            config_path = f.name

        try:
            os.environ["CONFIG_PATH"] = config_path
            import importlib
            import project_loader
            importlib.reload(project_loader)

            account_id = project_loader.get_billing_account_id()
            assert account_id == "AABBCC-DDEEFF-001122"
        finally:
            os.unlink(config_path)
            del os.environ["CONFIG_PATH"]

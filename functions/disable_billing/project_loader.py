import json
import logging
import os

logger = logging.getLogger(__name__)

CONFIG_PATH = os.environ.get("CONFIG_PATH", "./config/projects.json")


def _load_config() -> dict:
    """Load and parse the config file."""
    try:
        with open(CONFIG_PATH, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        logger.error(f"Config file not found: {CONFIG_PATH}")
        return {}
    except json.JSONDecodeError:
        logger.error(f"Invalid JSON in config file: {CONFIG_PATH}")
        return {}


def load_projects() -> list[dict]:
    """Load the list of managed projects from config."""
    config = _load_config()
    return config.get("projects", [])


def get_billing_account_id() -> str:
    """Get the billing account ID from config."""
    config = _load_config()
    return config.get("billing_account_id", "")

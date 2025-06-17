import os
import yaml
from typing import Tuple, Dict, Any


def load_config(config_path: str = "config.yml") -> Tuple[Dict[str, Any], str]:
    """
    Load a YAML configuration file.
    """
    abs_config_path = os.path.abspath(config_path)
    config_dir = os.path.dirname(abs_config_path)

    with open(abs_config_path, "r", encoding="utf-8") as f:  # UTF-8 for special characters support
        config = yaml.safe_load(f)

    return config, config_dir


def resolve_path(path: str, base_dir: str) -> str:
    """
    Resolve a path relative to a base directory if it's not absolute.

    Args:
        path (str): The target path to resolve.
        base_dir (str): The base directory to resolve against.

    Returns:
        str: The resolved absolute path.
    """
    if os.path.isabs(path):
        return path
    return os.path.normpath(os.path.join(base_dir or ".", path))
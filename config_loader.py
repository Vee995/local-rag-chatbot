import os
import yaml

def load_config(config_path="config.yml"):
    """
    Load YAML config from given path and return dict.
    Also returns the config directory for relative path resolution.
    """
    abs_config_path = os.path.abspath(config_path)
    config_dir = os.path.dirname(abs_config_path)
    
    with open(abs_config_path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
        
    return config, config_dir


def resolve_path(path, base_dir):
    """
    Resolve a potentially relative path against base_dir.
    If path is absolute, returns as is.
    """
    if os.path.isabs(path):
        return path
    return os.path.abspath(os.path.join(base_dir, path))
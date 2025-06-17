import os
from typing import Dict, Any
from loguru import logger
from utils.config_loader import resolve_path


def load_prompt_template(config: Dict[str, Any], config_dir: str) -> str:
    """
    Load the prompt template content based on prompt type from config.

    Args:
        config (Dict[str, Any]): Loaded configuration dictionary.
        config_dir (str): Path to the directory containing the config file.

    Returns:
        str: The content of the selected prompt template.
    """
    prompt_type = config.get("prompt_type", "basic") # basic is set as the deafult
    prompt_folder = config.get("prompt_folder")

    # Map prompt types to corresponding filenames
    prompt_files = {
        "basic": "prompt_zero.txt",
        "fewshot": "prompt_fewshot.txt",
        "cot": "prompt_cot.txt",
        "chaining": "prompt_chaining.txt",
    }

    prompt_filename = prompt_files.get(prompt_type, "prompt_zero.txt")
    prompt_path = resolve_path(os.path.join(prompt_folder, prompt_filename), config_dir)

    logger.info(f"Loading prompt template [{prompt_type}] from: {prompt_path}")
    # Ensure compatibility with non-ASCII characters
    with open(prompt_path, "r", encoding="utf-8") as f:
        return f.read()
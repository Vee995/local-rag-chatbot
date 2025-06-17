from typing import Any
from loguru import logger
from langchain_community.llms import Ollama


def load_llm(config: dict[str, Any]) -> Ollama:
    """
    Initialize and return an Ollama LLM instance based on configuration.

    Args:
        config (dict): Configuration dictionary containing LLM settings.

    Returns:
        Ollama: An initialized Ollama language model.
    """
    model_name = config.get("llm", {}).get("model", "mistral")
    logger.info(f"Initializing Ollama LLM with model: {model_name}")
    return Ollama(model=model_name)
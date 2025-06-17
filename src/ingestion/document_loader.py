import os
from typing import List, Any
from loguru import logger
from langchain.document_loaders import PyMuPDFLoader, TextLoader


def load_documents(config: dict, config_dir: str) -> List[Any]:
    """
    Load documents from a specified directory based on supported file types.

    Args:
        config (dict): Configuration dictionary with ingestion settings.
        config_dir (str): Base directory path for config-related files.

    Returns:
        List[Any]: List of loaded documents.
    """
    data_dir = os.path.join(config_dir, config["ingestion"]["data_dir"])
    supported_filetypes = config["ingestion"]["supported_filetypes"]

    logger.debug(f"Resolved data directory: {data_dir}")
    logger.debug(f"Supported file types: {supported_filetypes}")

    docs = []
    for filename in os.listdir(data_dir):
        path = os.path.join(data_dir, filename)
        logger.debug(f"Processing file: {filename}")

        # Load PDF files if supported
        if filename.endswith(".pdf") and ".pdf" in supported_filetypes:
            logger.info(f"Loading PDF document: {filename}")
            docs.extend(PyMuPDFLoader(path).load())
        # Load text files if supported
        elif filename.endswith(".txt") and ".txt" in supported_filetypes:
            logger.info(f"Loading text document: {filename}")
            docs.extend(TextLoader(path).load())
            
        # Skip files with unsupported extensions
        else:
            logger.warning(f"Skipping unsupported file: {filename}")

    return docs
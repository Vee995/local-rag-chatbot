from typing import List, Dict, Any
from loguru import logger
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document


def split_documents(docs: List[Document], config: Dict[str, Any]) -> List[Document]:
    """
    Split documents into smaller chunks using RecursiveCharacterTextSplitter.

    Args:
        docs (List[Document]): List of documents to split.
        config (Dict[str, Any]): Configuration containing chunk_size and chunk_overlap.

    Returns:
        List[Document]: List of split document chunks.
    """
    chunk_size = config["splitter"]["chunk_size"]
    chunk_overlap = config["splitter"]["chunk_overlap"]
    logger.debug(f"Using chunk_size={chunk_size}, chunk_overlap={chunk_overlap}")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
    chunks = splitter.split_documents(docs)
    logger.info(f"Split documents into {len(chunks)} chunks")

    return chunks
from typing import Any, Dict, List
from loguru import logger
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_core.documents import Document
from langchain.embeddings.base import Embeddings
from langchain.vectorstores.base import VectorStore
from utils.config_loader import resolve_path


def create_embedding(config: Dict[str, Any]) -> Embeddings:
    """
    Create and return an embedding model using the config settings.
    """
    model_name = config.get("embedding", {}).get("model_name", "all-MiniLM-L6-v2")
    logger.info(f"Creating embedding model: {model_name}")
    return SentenceTransformerEmbeddings(model_name=model_name)


def create_vectorstore_from_docs(
    config: Dict[str, Any],
    config_dir: str,
    docs: List[Document],
    embedding: Embeddings
) -> VectorStore:
    """
    Create and persist a Chroma vector store from documents.
    """
    persist_dir = resolve_path(
        config.get("vectorstore", {}).get("persist_directory", "chroma_db"),
        config_dir
    )
    logger.info(f"Creating and persisting vectorstore at: {persist_dir}")
    return Chroma.from_documents(docs, embedding, persist_directory=persist_dir)


def load_vectorstore(config: Dict[str, Any], config_dir: str) -> VectorStore:
    """
    Load an existing Chroma vector store.
    """
    # Load embedding model used when the vector store was created
    embedding_model = config.get("embedding", {}).get("model_name", "all-MiniLM-L6-v2")
    logger.info(f"Loading embedding model: {embedding_model}")
    embedding = SentenceTransformerEmbeddings(model_name=embedding_model)

    persist_dir = resolve_path(
        config.get("vectorstore", {}).get("persist_directory", "chroma_db"),
        config_dir
    )
    logger.info(f"Loading existing vectorstore from: {persist_dir}")
    return Chroma(persist_directory=persist_dir, embedding_function=embedding)
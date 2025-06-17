from loguru import logger
from utils.config_loader import load_config
from utils.logger_setup import setup_logging
from ingestion.document_loader import load_documents
from ingestion.text_splitter import split_documents
from vectorstore.embedding_store import create_embedding, create_vectorstore_from_docs


def ingest(config_path: str = "config.yml") -> None:
    """
    Perform document ingestion:
    1. Load documents from configured source
    2. Split documents into chunks
    3. Create embeddings and build/persist vector store

    Args:
        config_path (str): Path to the config YAML file. Defaults to "config.yml".
    """
    config, config_dir = load_config(config_path)
    setup_logging(config)

    docs = load_documents(config, config_dir)
    if not docs:
        logger.warning("No documents loaded. Exiting ingestion.")
        return

    # Split documents into manageable chunks for embedding
    chunks = split_documents(docs, config)
    if not chunks:
        logger.warning("No chunks created. Exiting ingestion.")
        return
    
    # Create embeddings and initialize vector store
    embedding = create_embedding(config)
    vectordb = create_vectorstore_from_docs(config, config_dir, chunks, embedding)
    vectordb.persist()
    logger.info("Vector store persisted successfully.")


if __name__ == "__main__":
    ingest()
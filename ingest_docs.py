import os
import sys
from loguru import logger
from config_loader import load_config, resolve_path
from langchain.document_loaders import PyMuPDFLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import SentenceTransformerEmbeddings

def ingest(config_path="config.yml"):
    config, config_dir = load_config(config_path)
    
    # Setup logging (console only)
    logger.remove()
    log_level = config.get("logging", {}).get("level", "INFO")
    logger.add(sys.stderr, level=log_level)
    logger.info(f"Logging initialized at level: {log_level}")
    
    data_dir = config.get("ingestion", {}).get("data_dir", "data")
    data_dir = resolve_path(data_dir, config_dir)
    logger.debug(f"Resolved data directory: {data_dir}")

    supported_filetypes = config.get("ingestion", {}).get("supported_filetypes", [".pdf", ".txt"])
    logger.debug(f"Supported file types: {supported_filetypes}")

    docs = []
    for filename in os.listdir(data_dir):
        path = os.path.join(data_dir, filename)
        logger.debug(f"Processing file: {filename}")

        if filename.endswith(".pdf") and ".pdf" in supported_filetypes:
            logger.info(f"Loading PDF document: {filename}")
            docs += PyMuPDFLoader(path).load()
        elif filename.endswith(".txt") and ".txt" in supported_filetypes:
            logger.info(f"Loading text document: {filename}")
            docs += TextLoader(path).load()
        else:
            logger.warning(f"Skipping unsupported file: {filename}")

    splitter_config = config.get("splitter", {})
    chunk_size = splitter_config.get("chunk_size", 500)
    chunk_overlap = splitter_config.get("chunk_overlap", 50)
    logger.debug(f"Using chunk_size={chunk_size}, chunk_overlap={chunk_overlap}")

    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    chunks = splitter.split_documents(docs)
    logger.info(f"Split documents into {len(chunks)} chunks")

    embedding_model = config.get("embedding", {}).get("model_name", "all-MiniLM-L6-v2")
    logger.info(f"Using embedding model: {embedding_model}")
    embedding = SentenceTransformerEmbeddings(model_name=embedding_model)

    persist_dir = config.get("vectorstore", {}).get("persist_directory", "chroma_db")
    persist_dir = resolve_path(persist_dir, config_dir)
    logger.debug(f"Persist directory resolved to: {persist_dir}")

    vectordb = Chroma.from_documents(chunks, embedding, persist_directory=persist_dir)
    vectordb.persist()
    logger.info("Vector store persisted successfully")

if __name__ == "__main__":
    ingest()

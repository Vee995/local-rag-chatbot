import sys
from loguru import logger
from config_loader import load_config, resolve_path
from langchain_community.llms import Ollama
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import SentenceTransformerEmbeddings

def get_rag_chain(config_path="config.yml"):
    config, config_dir = load_config(config_path)

    # Setup logging (console only)
    logger.remove()
    log_level = config.get("logging", {}).get("level", "INFO")
    logger.add(sys.stderr, level=log_level)
    logger.info(f"Logging initialized at level: {log_level}")

    prompt_path = config.get("prompt_path", "prompt.txt")
    prompt_path = resolve_path(prompt_path, config_dir)
    logger.info(f"Loading prompt template from: {prompt_path}")
    with open(prompt_path, "r", encoding="utf-8") as f:
        prompt_template_str = f.read()

    llm_config = config.get("llm", {})
    model_name = llm_config.get("model", "mistral")
    logger.info(f"Initializing Ollama LLM with model: {model_name}")
    llm = Ollama(model=model_name)

    embedding_model = config.get("embedding", {}).get("model_name", "all-MiniLM-L6-v2")
    logger.info(f"Using embedding model: {embedding_model}")
    embedding = SentenceTransformerEmbeddings(model_name=embedding_model)

    persist_dir = config.get("vectorstore", {}).get("persist_directory", "chroma_db")
    persist_dir = resolve_path(persist_dir, config_dir)
    logger.info(f"Loading vectorstore from directory: {persist_dir}")
    vectordb = Chroma(persist_directory=persist_dir, embedding_function=embedding)

    retriever = vectordb.as_retriever()
    logger.info("Retriever created from vectorstore")

    prompt_variables = config.get("prompt_variables", ["context", "question"])
    logger.debug(f"Prompt variables set: {prompt_variables}")

    prompt_template = PromptTemplate(
        input_variables=prompt_variables,
        template=prompt_template_str
    )

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        chain_type_kwargs={"prompt": prompt_template}
    )
    logger.info("RAG chain (RetrievalQA) created successfully")

    return qa_chain
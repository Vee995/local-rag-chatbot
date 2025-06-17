from typing import Any, Tuple
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from chatbot.llm_factory import load_llm
from prompts.prompt_loader import load_prompt_template
from utils.config_loader import load_config
from utils.logger_setup import setup_logging
from vectorstore.embedding_store import load_vectorstore

def get_rag_chain(config_path: str = "config.yml") -> RetrievalQA:
    """
    Create and return a Retrieval-Augmented Generation (RAG) chain.

    This function loads the configuration, sets up logging, loads
    the prompt template, initializes the LLM and vector store,
    then creates a RetrievalQA chain with the specified prompt.

    Args:
        config_path (str): Path to the YAML configuration file.

    Returns:
        RetrievalQA: Configured RetrievalQA chain instance.
    """
    config, config_dir = load_config(config_path)
    setup_logging(config)

    vectordb = load_vectorstore(config, config_dir)
    retriever = vectordb.as_retriever()

    prompt_template_str = load_prompt_template(config, config_dir)
    llm = load_llm(config)

    chain_type = config.get("chain", {}).get("type", "stuff")
    

    prompt_variables = config.get("prompt_variables", ["context", "question"])
    prompt_template = PromptTemplate(
        input_variables=prompt_variables,
        template=prompt_template_str,
    )

    # Build and return the RetrievalQA chain
    return RetrievalQA.from_chain_type(
        llm=llm,
        chain_type=chain_type,
        retriever=retriever,
        chain_type_kwargs={"prompt": prompt_template},
    )

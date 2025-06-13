import yaml
from langchain_community.llms import Ollama
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import SentenceTransformerEmbeddings

def get_rag_chain(config_path="config.yaml"):
    # Load config
    with open(config_path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    prompt_path = config.get("prompt_path", "prompt.txt")

    # Load prompt template
    with open(prompt_path, "r", encoding="utf-8") as f:
        prompt_template_str = f.read()

    llm = Ollama(model="mistral")  # Make sure Ollama is running

    embedding = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
    vectordb = Chroma(persist_directory="chroma_db", embedding_function=embedding)
    retriever = vectordb.as_retriever()

    prompt_template = PromptTemplate(
        input_variables=["context", "question"],
        template=prompt_template_str
    )

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        chain_type_kwargs={"prompt": prompt_template}
    )

    return qa_chain
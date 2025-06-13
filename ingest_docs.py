import os
from langchain.document_loaders import PyMuPDFLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import SentenceTransformerEmbeddings

def ingest():
    docs = []
    for filename in os.listdir("data"):
        path = os.path.join("data", filename)
        if filename.endswith(".pdf"):
            docs += PyMuPDFLoader(path).load()
        elif filename.endswith(".txt"):
            docs += TextLoader(path).load()

    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_documents(docs)

    embedding = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
    vectordb = Chroma.from_documents(chunks, embedding, persist_directory="chroma_db")
    vectordb.persist()

if __name__ == "__main__":
    ingest()
# local-rag-chatbot - TBU
A local Retrieval-Augmented Generation (RAG) chatbot using free Python tools, LangChain, llama-cpp-python, and Chroma.

# local-rag-chatbot-ollama -TBU

A local Retrieval-Augmented Generation (RAG) chatbot using Ollama LLM, Python, LangChain, ChromaDB, and Gradio.

---

## Overview

This project demonstrates how to build a local RAG pipeline that:

- Ingests documents (PDFs and text files)
- Embeds document chunks using Sentence Transformers
- Stores embeddings in a local Chroma vector database
- Retrieves relevant documents on user queries
- Generates answers using the Ollama local LLM server (e.g., Mistral)
- Provides an interactive chat UI with Gradio

---

## Prerequisites
Before you begin, make sure you have the following installed and set up:
- Python 3.9+ (Python 3.10+ recommended)
- Ollama — local LLM server (download from https://ollama.com/download)
- Git (optional, for cloning the repo)
- Virtual environment tool such as venv for Python dependency isolation
- Basic familiarity with command line / terminal usage

---
## Setup and Getting Started
Follow these steps to set up the project and start your local RAG chatbot:

### 1. Start Ollama 
- Start the Ollama server in a terminal:
    ```bash
    ollama run mistral # model name
    ```
- You can run `ollama list` to list all the models you have available locally in your Ollama environment.

### 2. Activate the virtual environment
- Run the following: 
    ```bash
    python -m venv venv # or py -3.12 -m venv venv (version specific)
    ```
- Proceed to activate the environment:
    ```bash
    .\venv\Scripts\activate
    ```
- To deactivate run the following:
    ```bash
    deactivate
    ```

### 3. Install dependices
- Run the following: `pip install -r requirements.txt`

### 4. Add your documents
- Place `PDFs` or `.txt` files into the `data/` folder.
- A sample folder inside `data/` contains two yoga PDFs you can use to test the setup.

### 5. Ingest documents
- Run the following from the `root` directory:
    ```bash
    python src/ingestion/ingest_documents.py
  ```

### 6. Run the chatbot UI
- Run the chatbot from the`root` directory and view using Gradio:
```bash
    python src/app.py
```
- Open http://127.0.0.1:7860 in your browser to chat.

## Tech Stack

- Ollama (LLM backend)
- LangChain (chaining + retrieval)
- Sentence-Transformers (embeddings)
- Chroma (vector DB)
- PyMuPDF (PDF ingestion)
- Gradio (web UI)
- Python 3.x on Windows

---

## Setup Instructions

### 1. Install Ollama

Download and install Ollama from [https://ollama.com/download](https://ollama.com/download).  
Start the Ollama server in a terminal:

```bash
ollama run mistral
```

### 2. Activate the virtual environment
python -m venv venv
py -3.12 -m venv venv (version specfic)
.\venv\Scripts\activate

### 3. Install dependencies:
pip install -r requirements.txt

### 4. Add your documents
Place PDFs or .txt files into the data/ folder.

### 5. Ingest documents
python ingest_docs.py

### 6. Run the chatbot UI
- Run the chatbot from the`root` directory and view using Gradio:
```bash
    python src/app.py
```
- Open http://127.0.0.1:7860 in your browser to chat.

Retrieval: Searching your documents for relevant context

Augmented Generation: Using an LLM to answer based on that context

Here’s the workflow:

Documents are split and embedded

Embeddings are stored in Chroma vector DB

User query triggers a semantic search to find relevant chunks

Relevant chunks + query are passed to Ollama LLM

Ollama generates a context-aware response

How does this make the LLM specific?
Retrieval step:

When a user asks a question, RAG first searches your indexed documents to find the most relevant snippets or chunks related to that question.

This retrieval uses embeddings (vector representations) to find close matches semantically.

Context feeding:

The retrieved documents (context) are passed alongside the user’s question into the LLM prompt.

The LLM “sees” the specific context, so it can generate answers based on your own data, not just its general training.

Response generation:

The LLM generates an answer conditioned on this fresh, specific information.

This means the output can be accurate, up-to-date, and domain-specific.

Why this matters
Without RAG, LLMs can hallucinate or give generic answers because they rely on fixed training data.

With RAG, your LLM can act as a smart search + summarization engine tuned exactly to your documents.

This enables applications like intelligent chatbots, expert assistants, or any AI that “knows your stuff.”


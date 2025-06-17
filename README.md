
Fully Free and Local — A Foundation for Production
Fully Free & Open Source:
This project uses only free and open-source tools and models that run entirely on your local machine — no paid cloud services or subscriptions required. You maintain full control over your data and environment.

Local-First Design:
All document ingestion, embedding, retrieval, and LLM inference happen locally. This keeps your data private and avoids cloud latency or costs.

Educational Foundation for Production:
While designed for local use and experimentation, this project’s architecture and components closely mirror patterns used in enterprise-level deployments.
For example, the same concepts apply when you move to managed services like AWS SageMaker, Amazon OpenSearch, or AWS Lambda for scaling and production robustness.

Easily Adaptable:
This project provides a solid understanding of retrieval-augmented generation (RAG) pipelines, prompt engineering, observability, and vector stores — all essential skills for building and migrating to production-grade AI applications.

Beginner-Friendly and Fun:
Primarily, this project is a learning tool to help you understand the basics of LLMs, RAG pipelines, and prompt engineering — perfect for experimentation, exploration, and having fun while getting hands-on with AI.




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

## What This Project Offers
- Build a fully local RAG chatbot using free open-source tools and models
- Ingest and chunk documents (PDF and text)
- Generate embeddings and store them in a persistent local vector store
- Query using semantic search combined with a local or remote LLM
- Experiment with prompt engineering and retrieval chain customization
- Integrated observability via Langsmith for tracing prompts and responses

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

- To stop ollama in your terminal, run: `/bye`

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

---

## Tools Used & Setup
This project leverages several powerful tools and libraries to build a local RAG chatbot:

### LangChain
- The core framework for chaining language model components and building the retrieval-augmented pipeline.

### Ollama (LLM backend)
- Provides the local large language model server (e.g., Mistral) used for generation.
- Setup: Download and install from ollama.com, then start the server with `ollama run mistral`.

### Chroma DB
- Vector database to store and query embeddings for fast semantic search.
- Setup: Included in `requirements.txt (chromadb)`, no separate setup required.

### Sentence-Transformers
- Used for generating vector embeddings of document chunks.

### Gradio
- Provides the interactive web UI for the chatbot.

### Loguru
- Easy-to-use logging library to capture and display logs.

### Langsmith
- (Optional) Observability and tracing for LangChain runs. Enable via config if needed.

### Pytest
- Testing framework for running automated tests.

---
Langsmith (Observability & Tracing)
Langsmith helps you monitor and trace your LangChain runs for better debugging and insights.

Requirements:
You need to create an account on Langsmith.

Setup:

Obtain your API key from Langsmith.

Create an .env file in your project root (or update it) with your API key:

env
Copy
Edit
LANGSMITH_API_KEY=your_api_key_here
See the included .env_sample file for reference.

Enable Langsmith in your config.yml by setting the appropriate flags and API key usage.

Make sure to restart your app after configuration changes to enable tracing





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


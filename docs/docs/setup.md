# Setup and Installation Guide

## Pre-requisites

Before you begin, ensure you have the following installed and set up:

- Python 3.9+ (Python 3.10+ recommended)  
- Ollama — local LLM server (download from [https://ollama.com/download](https://ollama.com/download))  
- Git (optional, for cloning the repo)  
- Virtual environment tool such as `venv` for Python dependency isolation  
- Basic familiarity with command line / terminal usage  

---

## Setup and Getting Started
Follow these steps to set up the project and start your local RAG chatbot:

### 1. Start Ollama 
- Start the Ollama server in a terminal:
    ```bash
    ollama run <model-name> # add model name e.g: mistral
    ```
- You can run `ollama list` to list all the models you have available locally in your Ollama environment.

- To stop ollama in your terminal, run: `/bye`

### 2. Activate the virtual environment
- Run the following: 
    ```python
    python -m venv venv # or py <add-python-version> -m venv venv (version specific e.g:-3.12)
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
- Run the following: 
    ```bash
    pip install -r requirements.txt
    ```

### 4. Add your documents
- Place `PDFs` or `.txt` files into the `data/` folder.
- A sample folder inside `data/` contains two yoga PDFs you can use to test the setup.

### 5. Ingest documents
- Run the following from the `root` directory:
    ```python
    python src/ingestion/ingest_documents.py
    ```

### 6. Run the chatbot UI
- Run the chatbot from the`root` directory and view using Gradio:
    ```python
    python src/app.py
    ```
- Open http://127.0.0.1:7860 in your browser to chat.

---

## Customizing Chakra Karen: Config and Project Updates

If you want to adapt Chakra Karen beyond its default yoga focus, here’s how you can update the project:

### 1. Expand or Change Karen’s Knowledge Base
- Add new documents (PDFs, `.txt` files) to the `data/` folder.  Examples: star signs, astrology, or any other specialty. <br><br> 
- Update Karen’s **personality and specialty** by editing prompt templates inside the `prompt_engineering/` folder (currently yoga-focused). <br><br> 
- Adjust the Gradio UI to fit your new domain by modifying `src/app.py`. <br><br> 
- Modify content guardrails (e.g., banned words/topics) within the `prompt_engineering/` folder and `config.yml`.

---

### 2. Update Prompt Engineering
- Add or modify prompt templates and variables directly in the `prompt_engineering/` folder. <br><br> 
- Change how Karen interacts by tweaking prompt logic here.

---

### 3. Basic Configuration Changes
- Edit `config.yml` to adjust: 
    - Model settings (model name, temperature)
    - Prompt types (`basic`, `fewshot`, `cot`, `chaining`)
    - LLM providers (e.g., Ollama, OpenAI, etc.)

---

### 4. Guardrails Configuration
- Basic content moderation is implemented via:  
  - Prompt templates in `prompt_engineering/` <br><br> 
  - Settings in `config.yml` (banned words/topics, max response length)  <br><br> 
- Update these as needed for your domain. <br><br> 

---

### 5. Enable Langsmith Tracing (Optional)

Langsmith tracing provides detailed logs to monitor and debug your chatbot’s prompt usage.

- By default, tracing is **disabled** (`enabled: false` in `config.yml`).  <br><br> 
- To enable:  
  1. Set `enabled: true` in the `langsmith` section of `config.yml`.  
  2. Create a `.env` file in the project root with your Langsmith API key and project name (see `.env.sample` for format).  
  3. Restart your app to apply changes.

> **Viewing traces:**  
> Log into [Langsmith](https://www.langchain.com/langsmith), select your project, and explore detailed traces of prompts, model outputs, and usage metrics.


---

## Set up Langsmith

1. **Create a Langsmith Account**  
   - Visit [Langsmith website](https://www.langchain.com/langsmith) and sign up for an account.

2. **Get Your API Key**  
   - After logging in, navigate to your user dashboard and go to settings on the left bottom pane. <br><br> 
   - Generate a new API key. Keep this key secure and do not share publicly.

3. **Create a `.env` File**  
   - In the root of your project, create a file named `.env`.  <br><br> 
   - Add your Langsmith API key and project name (see `env_sample`) <br><br> 
   - Replace `"your_langsmith_api_key_here"` with your actual API key.  <br><br> 
   - The `LANGCHAIN_PROJECT` name should match the one set in your `config.yml` under `langsmith.project`.

4. **Enable Langsmith in `config.yml`**  
   - Set `langsmith.enabled: true` in your `config.yml`.

5. **Restart Your Application**  
   - Restart the app to apply tracing.

6. **View Traces**
    - Navigate to your project dashboard using the project name you configured (e.g:`chakra-karen-chatbot-traces`).  <br><br> 
    - Here you can explore all recorded traces, including prompts, responses, and any errors or performance metrics. <br><br>  
    - Use filters and search tools to analyze specific chains, prompt versions, or user sessions to improve your chatbot’s performance.

---

> ⚠️ **Security Tip:** Never commit your `.env` file to public repositories. Add `.env` to your `.gitignore` to keep your secrets safe (by default, this has been added)
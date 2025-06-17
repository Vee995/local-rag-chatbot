import gradio as gr
import os
import random
from loguru import logger
from utils.config_loader import load_config
from chatbot.rag_chain import get_rag_chain
from utils.logger_setup import setup_logging  # <-- import your setup function
from dotenv import load_dotenv

load_dotenv()

# Load config
config, _ = load_config("config.yml")

# ---- Logging Setup ----
setup_logging(config)  # <-- centralized logger setup

langsmith_config = config.get("langsmith", {})
langsmith_enabled = langsmith_config.get("enabled", False)
project_name = langsmith_config.get("project", "default")

if langsmith_enabled:
    os.environ["LANGCHAIN_TRACING_V2"] = "true"
    os.environ["LANGCHAIN_PROJECT"] = project_name
else:
    os.environ["LANGCHAIN_TRACING_V2"] = "false"

# ---- Guardrails Setup ----
guardrails = config.get("guardrails", {})
banned_words = guardrails.get("banned_words", [])
banned_topics = guardrails.get("banned_topics", [])
messages = guardrails.get("messages", {})

# Get chain
chain = get_rag_chain(config_path="config.yml")


# ---- Chatbot Function ----
def chatbot_fn(question):
    question_lower = question.lower()
    logger.debug(f"Received question: {question}")

    if any(word in question_lower for word in banned_words):
        response = random.choice(
            messages.get("banned_word", ["Language, please. I'm in a Zen state. 🧘‍♀️"])
        )
        logger.warning(f"Banned word detected. Responding with: {response}")
        return response

    if any(topic in question_lower for topic in banned_topics):
        response = random.choice(
            messages.get(
                "banned_topic",
                ["Nice try 😏 but I’m not touching that topic with a yoga mat."],
            )
        )
        logger.warning(f"Banned topic detected. Responding with: {response}")
        return response

    response = chain.run(question)
    logger.debug("Response generated via chain.")
    return response


# ---- Gradio Interface ----
gr.Interface(
    fn=chatbot_fn,
    inputs=gr.Textbox(lines=2, placeholder="Ask Karen any question about yoga..."),
    outputs="text",
    title="🧘‍♀️Chakra Karen: My third eye rolls... a lot",
    description="Ask Chakra Karen anything about yoga, chakras, or how to stay zen (or not). She’s mean but informative!",
).launch()
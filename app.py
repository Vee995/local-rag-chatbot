import gradio as gr
import random
import sys
from loguru import logger
from config_loader import load_config
from rag_chain import get_rag_chain

# Load config
config, _ = load_config("config.yml")

# ---- Logging Setup ----
logger.remove()  # Remove default Loguru handler

logging_config = config.get("logging", {})
log_level = logging_config.get("level", "INFO")  # Default to INFO if not set

# Log to console only
logger.add(sys.stderr, level=log_level)
logger.info("Console logging initialized.")

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
        response = random.choice(messages.get("banned_word", ["Language, please. I'm in a Zen state. 🧘‍♀️"]))
        logger.warning(f"Banned word detected. Responding with: {response}")
        return response

    if any(topic in question_lower for topic in banned_topics):
        response = random.choice(messages.get("banned_topic", ["Nice try 😏 but I’m not touching that topic with a yoga mat."]))
        logger.warning(f"Banned topic detected. Responding with: {response}")
        return response

    response = chain.run(question)
    logger.debug("Response generated via chain.")
    return response

# ---- Gradio Interface ----
gr.Interface(
    fn=chatbot_fn,
    inputs="text",
    outputs="text",
    title="🧘‍♀️ Om-egaBot – Your Yoga Sidekick"
).launch()

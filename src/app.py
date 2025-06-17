import os
import random
from typing import Optional
import gradio as gr
from dotenv import load_dotenv
from loguru import logger
from chatbot.rag_chain import get_rag_chain
from utils.config_loader import load_config
from utils.logger_setup import setup_logging


def initialize_environment(config: dict) -> None:
    """
    Initializes environment variables for Langsmith tracing based on config.
    """
    langsmith_config = config.get("langsmith", {})
    langsmith_enabled = langsmith_config.get("enabled", False)
    project_name = langsmith_config.get("project", "default")

    os.environ["LANGCHAIN_TRACING_V2"] = "true" if langsmith_enabled else "false"
    os.environ["LANGCHAIN_PROJECT"] = project_name


def get_guardrails(config: dict) -> tuple[list[str], list[str], dict]:
    """
    Extracts guardrails like banned words, topics, and messages from config.
    """
    guardrails = config.get("guardrails", {})
    banned_words = guardrails.get("banned_words", [])
    banned_topics = guardrails.get("banned_topics", [])
    messages = guardrails.get("messages", {})
    return banned_words, banned_topics, messages


def chatbot_fn(question: str) -> str:
    """
    Handles chatbot input, checks for banned content, and returns a response.

    Args:
        question (str): The user's question.

    Returns:
        str: The chatbot's response.
    """
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
    logger.debug("Response generated via RAG chain.")
    return response


if __name__ == "__main__":
    load_dotenv()
    config, _ = load_config("config.yml")
    setup_logging(config)
    initialize_environment(config)
    banned_words, banned_topics, messages = get_guardrails(config)
    chain = get_rag_chain(config_path="config.yml")

    # Launch Gradio Interface
    gr.Interface(
        fn=chatbot_fn,
        inputs=gr.Textbox(lines=2, placeholder="Ask Karen any question about yoga..."),
        outputs="text",
        title="🧘‍♀️ Chakra Karen: My third eye rolls... a lot",
        description="Ask Chakra Karen anything about yoga, chakras, or how to stay zen (or not). She’s mean but informative!",
    ).launch()

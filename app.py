import gradio as gr
import yaml
from rag_chain import get_rag_chain

# Load config.yaml
with open("config.yaml", "r", encoding="utf-8") as f:
    config = yaml.safe_load(f)

guardrails = config.get("guardrails", {})
banned_words = guardrails.get("banned_words", [])
banned_topics = guardrails.get("banned_topics", [])
messages = guardrails.get("messages", {})

chain = get_rag_chain()

def chatbot_fn(question):
    question_lower = question.lower()

    if any(word in question_lower for word in banned_words):
        return messages.get("banned_word", "Language, please. I'm in a Zen state. 🧘‍♀️")

    if any(topic in question_lower for topic in banned_topics):
        return messages.get("banned_topic", "Nice try 😏 but I’m not touching that topic with a yoga mat.")

    return chain.run(question)

gr.Interface(fn=chatbot_fn, inputs="text", outputs="text", title="🧘‍♀️ Om-egaBot – Your Yoga Sidekick").launch()

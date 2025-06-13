import gradio as gr
from rag_chain import get_rag_chain

chain = get_rag_chain()

def chatbot_fn(question):
    return chain.run(question)

gr.Interface(fn=chatbot_fn, inputs="text", outputs="text", title="Ollama RAG Chatbot").launch()

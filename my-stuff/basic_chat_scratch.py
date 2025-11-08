import libs.open_ai_chat_basic as oai_chat
import libs.llama_chat_basic as llama_chat
import gradio as gr






client = oai_chat.OpenAIChatClient(temperature=0.5, max_tokens=2000)
client.set_system_message("You are a helpful coding assistant. Keep your answers short and to the point.")
gr.ChatInterface(fn=client.chat_stream, type="messages").launch()

# client = llama_chat.LlamaChatClient()
# client.set_system_message("You are a helpful coding assistant.")
# gr.ChatInterface(fn=client.chat_stream, type="messages").launch()














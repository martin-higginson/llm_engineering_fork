import libs.open_ai_chat_basic as oai_chat
import libs.llama_chat_basic as llama_chat
import gradio as gr


system_message = "You are a helpful assistant for an Airline called FlightAI. "
system_message += "Give short, courteous answers, no more than 1 sentence. "
system_message += "Always be accurate. If you don't know the answer, say so."




# client = oai_chat.OpenAIChatClient(temperature=0.5, max_tokens=2000)
# client.set_system_message("You are a helpful coding assistant.")
# gr.ChatInterface(fn=client.chat_stream, type="messages").launch()

client = llama_chat.LlamaChatClient()
client.set_system_message("You are a helpful coding assistant.")
gr.ChatInterface(fn=client.chat_stream, type="messages").launch()














from typing import Annotated
from typing_extensions import TypedDict 
from langchain_groq import ChatGroq 
from langgraph.graph import StateGraph, START, END
from langgraph.graph import add_messages 
from langchain_core.messages import SystemMessage 
from dotenv import load_dotenv
import os 

load_dotenv()

groq_api_key = os.getenv("GROQ_API_KEY")
LANGCHAIN_API_KEY = os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"]="ai-therapist"

llm = ChatGroq(groq_api_key=groq_api_key, model_name = "Gemma2-9b-It")

system_prompt = SystemMessage(
    content = (
        "You are an AI therapist. You respond empathetically, calmly, and supportively. "
        "You do not diagnose or prescribe. You offer active listening, emotional validation, "
        "and gently guide the user toward reflection. Use a warm, conversational tone."
    )
)

class State(TypedDict):
    messages: Annotated[list,add_messages]

graph_builder = StateGraph(State)

def chatbot(state: State):
    history = state['messages']
    messages = [system_prompt]+history
    return {"messages":llm.invoke(messages)}

graph_builder.add_node("chatbot",chatbot)
graph_builder.add_edge(START,"chatbot")
graph_builder.add_edge("chatbot",END)

graph = graph_builder.compile()

def get_response(user_input, history):
    new_event = {"messages":("user",user_input)}
    full_history = history +[("user",user_input)]
    for event in graph.stream(new_event):
        for value in event.values():
            full_history.append(("ai", value["messages"].content.strip()))
            return value["messages"].content.strip(), full_history
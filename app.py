import streamlit as st
from main import get_response

st.set_page_config(page_title = "AI Therapist")
st.title("AI Therapist")
st.markdown("Talk to a calming and supportive AI therapist")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

user_input = st.chat_input("What's on your mind?")

if user_input:
    with st.spinner("Thinking..."):
        response , updated_history = get_response(user_input,st.session_state.chat_history)
        st.session_state.chat_history = updated_history

for role, message in st.session_state.chat_history:
    with st.chat_message("user" if role == "user" else "ai"):
        st.markdown(message)
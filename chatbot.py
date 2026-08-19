<<<<<<< HEAD
import streamlit as st
from utils import chat_with_law_bot

def chatbot_page():
    st.header("⚖️ Legal Chatbot")
    st.write("Ask questions about legal matters.")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    user_query = st.text_input("Enter your question:")

    if st.button("Ask"):
        if user_query.strip():
            with st.spinner("Generating response..."):
                response = chat_with_law_bot(user_query)
                st.session_state.chat_history.append(("You", user_query))
                st.session_state.chat_history.append(("Bot", response))

    st.markdown("### 🗨️ Conversation History")
    for role, message in st.session_state.chat_history:
        if role == "You":
            st.markdown(f'<div style="background-color:#DCF8C6; padding:10px; margin-bottom:10px; border-radius:10px; color:#000;">👤 {message}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div style="background-color:#EAEAEA; padding:10px; margin-bottom:10px; border-radius:10px; color:#000;">🤖 {message}</div>', unsafe_allow_html=True)
=======
import streamlit as st
from utils import chat_with_law_bot

def chatbot_page():
    st.header("⚖️ Legal Chatbot")
    st.write("Ask questions about legal matters.")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    user_query = st.text_input("Enter your question:")

    if st.button("Ask"):
        if user_query.strip():
            with st.spinner("Generating response..."):
                response = chat_with_law_bot(user_query)
                st.session_state.chat_history.append(("You", user_query))
                st.session_state.chat_history.append(("Bot", response))

    st.markdown("### 🗨️ Conversation History")
    for role, message in st.session_state.chat_history:
        if role == "You":
            st.markdown(f'<div style="background-color:#DCF8C6; padding:10px; margin-bottom:10px; border-radius:10px; color:#000;">👤 {message}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div style="background-color:#EAEAEA; padding:10px; margin-bottom:10px; border-radius:10px; color:#000;">🤖 {message}</div>', unsafe_allow_html=True)
>>>>>>> 778ca0525845585a232748686960a92a35626e59

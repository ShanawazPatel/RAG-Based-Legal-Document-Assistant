import streamlit as st
from summarizer import summarizer_page
from chatbot import chatbot_page
from document_generator import document_generator_page

def main():
    st.sidebar.title("🔍 Navigation")
    page = st.sidebar.radio("Go to:", ["Summarizer", "Chatbot", "Document Generator"])

    if page == "Summarizer":
        summarizer_page()
    elif page == "Chatbot":
        chatbot_page()
    else:
        document_generator_page()

if __name__ == "__main__":
    main()

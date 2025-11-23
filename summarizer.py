import streamlit as st
from utils import extract_text_from_pdf, summarize_text

def summarizer_page():
    st.header("📄 PDF Summarizer")
    st.write("Upload a PDF file to generate a summary.")

    uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"])

    if uploaded_file:
        with st.spinner("Extracting text..."):
            text = extract_text_from_pdf(uploaded_file)

        if text:
            st.success("Text extracted successfully!")
            if st.button("Summarize"):
                with st.spinner("Summarizing..."):
                    summary = summarize_text(text)
                    st.markdown("### Summary:")
                    st.write(summary)
        else:
            st.error("Failed to extract text from the PDF. Please try another file.")

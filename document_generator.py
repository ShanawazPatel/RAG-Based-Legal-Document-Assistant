import streamlit as st
from utils import generate_document, download_document

def document_generator_page():
    st.header("📜 Legal Document Generator")
    st.write("Select a document type and provide required details.")

    doc_type = st.selectbox("Choose Document Type", ["Legal Notice", "Contract Agreement", "Affidavit"])
    user_input = st.text_area("Enter details for the document:")

    if st.button("Generate Document"):
        if user_input.strip():
            doc = generate_document(doc_type, user_input)
            st.success(f"{doc_type} generated successfully!")
            download_document(doc, f"{doc_type}.pdf", "pdf")
        else:
            st.error("Please enter details for the document.")

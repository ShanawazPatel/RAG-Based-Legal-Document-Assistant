import logging
import io
import os
from pathlib import Path
from PyPDF2 import PdfReader
from langchain_ollama import ChatOllama
from fpdf import FPDF
from docx import Document
import streamlit as st

# Logging configuration
logging.basicConfig(level=logging.INFO)

MODEL_NAME = "gemma3:4b"
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://127.0.0.1:11434")

def extract_text_from_pdf(pdf_file):
    try:
        pdf_reader = PdfReader(pdf_file)
        text = "\n".join([page.extract_text() for page in pdf_reader.pages if page.extract_text()])
        return text.strip() if text else None
    except Exception as e:
        logging.error(f"Error extracting text from PDF: {str(e)}")
        return None

def summarize_text(text):
    try:
        llm = ChatOllama(model=MODEL_NAME, base_url=OLLAMA_BASE_URL)
        prompt = f"Summarize the following text in a clear and concise manner:\n\n{text}"
        response = llm.invoke(prompt)
        return response.content.strip() if hasattr(response, "content") else "Error: No summary generated."
    except Exception as e:
        logging.error(f"Error in summarization: {str(e)}")
        return f"Error generating summary: {str(e)}"

def chat_with_law_bot(user_query):
    try:
        llm = ChatOllama(model=MODEL_NAME, base_url=OLLAMA_BASE_URL)
        response = llm.invoke(user_query)
        return response.content.strip() if hasattr(response, "content") else "Error: No response generated."
    except Exception as e:
        logging.error(f"Error in chatbot: {str(e)}")
        return f"Error generating response: {str(e)}"

def generate_document(doc_type, doc_data):
    if doc_type not in ["Legal Notice", "Contract Agreement", "Affidavit"]:
        return None

    doc = Document()
    doc.add_heading("RAG Based Legal Document Assistant", level=1)
    doc.add_heading(doc_type, level=2)

    if doc_type == "Legal Notice":
        # Header
        court_header = doc_data.get('court_name') or "[Court Name]"
        jurisdiction = doc_data.get('jurisdiction') or "[Jurisdiction]"
        doc.add_heading(court_header + f", {jurisdiction}", level=1)
        doc.add_paragraph(f"Date: {doc_data.get('date', '')}")

        # Case / Recipient block
        if doc_data.get('case_title'):
            doc.add_paragraph(f"Case: {doc_data.get('case_title')} — Case No. {doc_data.get('case_no', '')}")
        doc.add_paragraph(f"To: {doc_data.get('recipient', '')}")
        doc.add_paragraph(f"Subject: {doc_data.get('subject', '')}")
        doc.add_paragraph("")

        # Main notice body
        doc.add_paragraph(doc_data.get('details', ''))
        doc.add_paragraph("")

        # Hearing / Location information
        hearing = doc_data.get('hearing_date')
        location = doc_data.get('location')
        if hearing or location:
            doc.add_paragraph("Proceeding Details:")
            if hearing:
                doc.add_paragraph(f"- Date / Time: {hearing}")
            if location:
                doc.add_paragraph(f"- Location / Access: {location}")
            doc.add_paragraph("")

        # Contact & service
        clerk_phone = doc_data.get('clerk_phone')
        clerk_email = doc_data.get('clerk_email')
        if clerk_phone or clerk_email:
            doc.add_paragraph("Contact for Questions:")
            if clerk_phone:
                doc.add_paragraph(f"Clerk Phone: {clerk_phone}")
            if clerk_email:
                doc.add_paragraph(f"Clerk Email: {clerk_email}")
            doc.add_paragraph("")

        # Signature
        doc.add_paragraph("Sincerely,")
        doc.add_paragraph("")
        doc.add_paragraph("_______________________________")
        prepared_by = doc_data.get('prepared_by')
        if prepared_by:
            doc.add_paragraph(prepared_by)
        else:
            doc.add_paragraph("[Name], [Title]")

        # About the Court section
        doc.add_heading("About the Court", level=3)
        about_lines = []
        about_lines.append(f"Name: {court_header}")
        about_lines.append(f"Jurisdiction: {jurisdiction}")
        if doc_data.get('court_address'):
            about_lines.append(f"Address: {doc_data.get('court_address')}")
        if doc_data.get('court_website'):
            about_lines.append(f"Website: {doc_data.get('court_website')}")
        about_lines.append("The Court adjudicates matters within its statutory jurisdiction and issues orders in accordance with applicable law.")
        about_lines.append("Hours: Monday–Friday, standard business hours. Contact the Clerk for specific schedules and accessibility accommodations.")
        for line in about_lines:
            doc.add_paragraph(line)

    elif doc_type == "Contract Agreement":
        doc.add_paragraph(f"Date: {doc_data['date']}")
        doc.add_paragraph(f"Party One: {doc_data['party_one']}")
        doc.add_paragraph(f"Party Two: {doc_data['party_two']}")
        doc.add_paragraph("")
        doc.add_paragraph(
            f"This Contract Agreement is entered into on {doc_data['date']} by and between {doc_data['party_one']} and {doc_data['party_two']}."
        )
        doc.add_paragraph("")
        doc.add_paragraph(doc_data['details'])
        if doc_data.get('term'):
            doc.add_paragraph("")
            doc.add_paragraph(f"Term: {doc_data['term']}")
        doc.add_paragraph("")
        doc.add_paragraph("_______________________________")
        doc.add_paragraph(f"{doc_data['party_one']}")
        doc.add_paragraph("")
        doc.add_paragraph("_______________________________")
        doc.add_paragraph(f"{doc_data['party_two']}")

    else:  # Affidavit
        doc.add_paragraph(f"Date: {doc_data['date']}")
        if doc_data.get('place'):
            doc.add_paragraph(f"Place of Declaration: {doc_data['place']}")
        doc.add_paragraph(f"Affiant: {doc_data['deponent']}")
        doc.add_paragraph("")
        doc.add_paragraph("I hereby declare the following:")
        doc.add_paragraph(doc_data['statement'])
        doc.add_paragraph("")
        doc.add_paragraph("I affirm that the foregoing is true and correct to the best of my knowledge.")
        doc.add_paragraph("")
        doc.add_paragraph("_______________________________")
        doc.add_paragraph(f"{doc_data['deponent']}")

    return doc


def format_preview_text(doc_type, doc_data):
    if doc_type == "Legal Notice":
        lines = [
            "Professional Notice",
            f"Date: {doc_data.get('date', '')}",
            f"To: {doc_data.get('recipient', '')}",
            f"Subject: {doc_data.get('subject', '')}",
            "",
            doc_data.get('details', ''),
            "",
        ]
        if doc_data.get('hearing_date') or doc_data.get('location'):
            lines.append("Proceeding Details:")
            if doc_data.get('hearing_date'):
                lines.append(f"- Date/Time: {doc_data.get('hearing_date')}")
            if doc_data.get('location'):
                lines.append(f"- Location/Access: {doc_data.get('location')}")
            lines.append("")
        lines.append("Sincerely,")
        prepared = doc_data.get('prepared_by') or "[Name], [Title]"
        lines.append(prepared)
        lines.append("")
        lines.append("About the Court:")
        lines.append(f"Name: {doc_data.get('court_name', '')}")
        lines.append(f"Jurisdiction: {doc_data.get('jurisdiction', '')}")
        if doc_data.get('court_website'):
            lines.append(f"Website: {doc_data.get('court_website')}")
        return "\n".join(lines)
    if doc_type == "Contract Agreement":
        return (
            f"RAG Based Legal Document Assistant\n\n"
            f"Contract Agreement\n"
            f"Date: {doc_data['date']}\n"
            f"Party One: {doc_data['party_one']}\n"
            f"Party Two: {doc_data['party_two']}\n\n"
            f"This Contract Agreement is entered into on {doc_data['date']} by and between {doc_data['party_one']} and {doc_data['party_two']}.\n\n"
            f"{doc_data['details']}\n\n"
            f"Term: {doc_data['term']}"
        )
    return (
        f"RAG Based Legal Document Assistant\n\n"
        f"Affidavit\n"
        f"Date: {doc_data['date']}\n"
        f"Place of Declaration: {doc_data.get('place', '')}\n"
        f"Affiant: {doc_data['deponent']}\n\n"
        f"I hereby declare the following:\n{doc_data['statement']}\n\n"
        "I affirm that the foregoing is true and correct to the best of my knowledge."
    )


def download_document(doc, filename, file_type):
    if file_type == "pdf":
        pdf = FPDF()
        pdf.set_auto_page_break(True, margin=15)
        pdf.add_page()

        # Use a Unicode-capable TTF font when available.
        font_path = Path(r"C:\Windows\Fonts\arial.ttf")
        if font_path.exists():
            pdf.add_font("ArialUnicode", "", str(font_path), uni=True)
            pdf.set_font("ArialUnicode", size=12)
        else:
            pdf.set_font("Arial", size=12)

        text = "\n\n".join([str(paragraph.text) for paragraph in doc.paragraphs if paragraph.text])
        if not text:
            text = "(No document content available)"

        pdf.multi_cell(0, 10, text)
        pdf_output = pdf.output(dest="S")
        pdf_bytes = pdf_output.encode("latin-1", "replace") if isinstance(pdf_output, str) else pdf_output
        st.download_button("📥 Download PDF", data=pdf_bytes, file_name=filename, mime="application/pdf")
    elif file_type == "docx":
        buffer = io.BytesIO()
        doc.save(buffer)
        st.download_button("📥 Download DOCX", data=buffer.getvalue(), file_name=filename, mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")

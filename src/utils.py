import logging
import os
import io
from typing import List, Tuple, Dict, Any, Optional
from PyPDF2 import PdfReader
from dotenv import load_dotenv

load_dotenv()

# Logging configuration
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def get_llm(provider: str = "Ollama", model_name: str = "llama3.2:1b", api_key: Optional[str] = None):
    """
    Model Router Factory: Supports local Ollama and Cloud LLM providers (Groq, OpenAI).
    """
    try:
        if provider == "Groq":
            from langchain_groq import ChatGroq
            key = api_key or os.getenv("GROQ_API_KEY")
            if not key:
                raise ValueError("Groq API key is missing. Please set GROQ_API_KEY in .env or pass it.")
            return ChatGroq(model_name=model_name or "llama-3.3-70b-versatile", groq_api_key=key, temperature=0.2)
        else: # Default to Ollama
            from langchain_ollama import ChatOllama
            base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
            return ChatOllama(model=model_name or "llama3.2:1b", base_url=base_url, temperature=0.2)
    except Exception as e:
        logging.error(f"Error initializing LLM model ({provider}): {str(e)}")
        # Fallback attempting default ChatOllama
        from langchain_ollama import ChatOllama
        return ChatOllama(model="llama3.2:1b")


def extract_pages_from_pdf(pdf_file) -> List[Dict[str, Any]]:
    """
    Extract text per page from a PDF file.
    Returns a list of dicts: [{'page': 1, 'text': '...'}, ...]
    """
    pages_data = []
    try:
        pdf_reader = PdfReader(pdf_file)
        for idx, page in enumerate(pdf_reader.pages):
            txt = page.extract_text()
            if txt and txt.strip():
                pages_data.append({
                    "page": idx + 1,
                    "text": txt.strip()
                })
    except Exception as e:
        logging.error(f"Error extracting PDF pages: {str(e)}")
    return pages_data


def extract_full_text_from_pdf(pdf_file) -> str:
    """
    Extract full text from a PDF file.
    """
    pages = extract_pages_from_pdf(pdf_file)
    return "\n\n".join([f"--- Page {p['page']} ---\n{p['text']}" for p in pages])


def extract_text_from_file(uploaded_file) -> str:
    """
    Extract text from PDF, DOCX, or TXT file stream.
    """
    if not uploaded_file:
        return ""
    name = getattr(uploaded_file, "name", "").lower()
    
    if name.endswith(".docx"):
        try:
            from docx import Document as DocxDoc
            doc = DocxDoc(uploaded_file)
            return "\n".join([p.text for p in doc.paragraphs if p.text.strip()])
        except Exception as e:
            logging.error(f"Error extracting docx: {e}")
            return ""
    elif name.endswith(".txt"):
        try:
            content = uploaded_file.read()
            if isinstance(content, bytes):
                return content.decode("utf-8", errors="replace")
            return str(content)
        except Exception as e:
            logging.error(f"Error extracting txt: {e}")
            return ""
    else:
        return extract_full_text_from_pdf(uploaded_file)

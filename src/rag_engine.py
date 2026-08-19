import os
import logging
from typing import List, Dict, Any, Tuple

try:
    from langchain_text_splitters import RecursiveCharacterTextSplitter
except ImportError:
    from langchain.text_splitter import RecursiveCharacterTextSplitter

from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

try:
    from langchain_core.documents import Document
except ImportError:
    from langchain.schema import Document

from src.utils import get_llm, extract_pages_from_pdf

logging.basicConfig(level=logging.INFO)

class LegalRAGEngine:
    def __init__(self, embedding_model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        """
        Initialize the RAG Engine with HuggingFace embeddings.
        """
        try:
            self.embeddings = HuggingFaceEmbeddings(model_name=embedding_model_name)
        except Exception as e:
            logging.warning(f"Error loading HuggingFaceEmbeddings ({e}), attempting fallback.")
            self.embeddings = None
        self.vector_store = None
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            separators=["\n\n", "\n", " ", ""]
        )

    def process_pdf_and_create_vectorstore(self, pdf_file, file_name: str = "document.pdf") -> int:
        """
        Extracts pages from PDF, chunks text preserving page numbers, and indexes into ChromaDB.
        Returns the total chunk count.
        """
        pages_data = extract_pages_from_pdf(pdf_file)
        if not pages_data:
            raise ValueError("No text could be extracted from the uploaded PDF file.")

        documents = []
        for p in pages_data:
            page_num = p["page"]
            text = p["text"]
            # Split text into chunks
            chunks = self.text_splitter.split_text(text)
            for chunk_idx, chunk in enumerate(chunks):
                doc = Document(
                    page_content=chunk,
                    metadata={
                        "source": file_name,
                        "page": page_num,
                        "chunk_id": f"p{page_num}_c{chunk_idx}"
                    }
                )
                documents.append(doc)

        # Create Chroma VectorStore
        if self.embeddings:
            self.vector_store = Chroma.from_documents(documents=documents, embedding=self.embeddings)
        else:
            raise RuntimeError("Embeddings model is not available.")

        return len(documents)

    def query(self, user_query: str, provider: str = "Ollama", model_name: str = "llama3.2:1b", top_k: int = 4) -> Dict[str, Any]:
        """
        Retrieves top_k chunks for user query, executes RAG prompt with citations.
        Returns dict containing answer, context chunks, and source page citations.
        """
        if not self.vector_store:
            return {
                "answer": "No document has been indexed yet. Please upload a PDF contract first.",
                "sources": [],
                "contexts": []
            }

        # 1. Similarity search
        retrieved_docs = self.vector_store.similarity_search(user_query, k=top_k)

        # 2. Format context with citations
        context_blocks = []
        sources = []
        for doc in retrieved_docs:
            page = doc.metadata.get("page", "Unknown")
            source_info = f"[Page {page}]"
            sources.append({
                "page": page,
                "snippet": doc.page_content[:250] + "..." if len(doc.page_content) > 250 else doc.page_content
            })
            context_blocks.append(f"--- Document Excerpt {source_info} ---\n{doc.page_content}")

        context_str = "\n\n".join(context_blocks)

        # 3. Formulate RAG Prompt
        prompt = f"""You are an expert Legal AI Assistant. Answer the user's question using ONLY the provided legal document excerpts below.
If the answer cannot be found in the context, explicitly state "I cannot find sufficient context in the document to answer this query."

Include page citations in your answer when referencing specific clauses.

DOCUMENT CONTEXT:
{context_str}

USER QUESTION: {user_query}

LEGAL ASSISTANT ANSWER (with page citations):"""

        # 4. Invoke LLM
        llm = get_llm(provider=provider, model_name=model_name)
        response = llm.invoke(prompt)
        answer = response.content.strip() if hasattr(response, "content") else str(response)

        return {
            "answer": answer,
            "sources": sources,
            "contexts": [doc.page_content for doc in retrieved_docs]
        }

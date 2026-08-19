# 📜 Enterprise AI Legal Assistant & Contract Auditor

An enterprise-grade, local **Retrieval-Augmented Generation (RAG)** platform designed to provide general AI legal advice, analyze legal contracts, perform clause-level risk audits, draft contracts and formal legal notices, and execute semantic contract comparisons.

![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-v0.1-1C3C3C?style=for-the-badge&logo=langchain&logoColor=white)
![ChromaDB](https://img.shields.io/badge/ChromaDB-Vector_DB-FF6F61?style=for-the-badge)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Ollama](https://img.shields.io/badge/Ollama-Local_LLM-000000?style=for-the-badge)
![Groq](https://img.shields.io/badge/Groq-Cloud_API-F05A28?style=for-the-badge)

---

## 🌟 Dedicated Application Modules

### 1️⃣ 🤖 Standalone AI Legal Chatbot
- Ask general legal questions, corporate compliance queries, or legal procedures.
- Powered by LLM legal prompt engineering with sample question quick-triggers.

### 2️⃣ 📚 Document RAG Assistant (Vector Search & Citations)
- **Vector Database:** Indexes legal PDF contracts using `ChromaDB` and `HuggingFaceEmbeddings` (`sentence-transformers/all-MiniLM-L6-v2`).
- **Semantic Text Chunking:** `RecursiveCharacterTextSplitter` chunks documents while maintaining page number metadata.
- **Source Citation:** Every answer cites the exact **page number** and text snippet from the contract.

### 3️⃣ 📜 Contract & Agreement Generator
- Form-driven AI generation for **Non-Disclosure Agreements (NDAs)**, **Employment Agreements**, **Independent Contractor Agreements**, and **Master Service Agreements**.
- Multi-format download in **Word (`.docx`)** and styled **PDF (`.pdf`)**.

### 4️⃣ ⚖️ Legal Notice & Affidavit Generator
- Form-driven drafting specifically for **Legal Notices (Breach of Contract, Payment Recovery, Eviction)** and **Sworn Affidavits**.
- Multi-format download in **Word (`.docx`)** and styled **PDF (`.pdf`)**.

### 5️⃣ 🔍 Automated Contract Risk Auditor
- **Risk Scoring:** Scans documents for high-risk clauses (Indemnification, Unlimited Liability, Strict Non-Compete, Termination Penalties).
- **Redline Suggestions:** Provides risk ratings (🔴 High / 🟡 Medium / 🟢 Low) with redlined amendments.

### 6️⃣ ⚔️ Semantic Contract Comparison
- **Version Diffing:** Upload two contract versions (Original vs Revised Draft).
- **Clause Audit:** Highlights added, deleted, or modified terms and assesses risk impact during negotiations.

---

## 🔧 Installation & Quickstart

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Launch application
streamlit run app.py
```

---

## 📄 License
Distributed under the **MIT License**.

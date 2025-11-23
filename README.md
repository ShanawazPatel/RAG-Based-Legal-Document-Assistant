# 📜 Legal Documents Assistant

Legal Documents Assistant is a **Streamlit-based AI tool** designed to help lawyers and legal professionals with **document generation, summarization, and legal chatbot assistance**. This project leverages **Ollama models** to provide AI-powered legal assistance.

## 🚀 Features

### 1️⃣ **PDF Summarizer**
- Upload **PDF** files and extract key insights.
- AI-powered text summarization.

### 2️⃣ **Legal Chatbot**
- Ask legal questions and get AI-generated responses.
- Maintains **conversation history**.

### 3️⃣ **Document Generator**
- Generate **Legal Notices, Contracts, and Affidavits**.
- Download documents in **PDF** and **DOCX** formats.

## 🏗️ Project Structure

```
/legal_assistant/
│── main.py                # Entry point for the app
│── summarizer.py          # PDF summarizer module
│── chatbot.py             # Legal chatbot module
│── document_generator.py  # Document generation module
│── utils.py               # Utility functions (PDF handling, AI models, etc.)
│── README.md              # Project documentation
```

## 🔧 Installation & Setup

### 1️⃣ **Clone the Repository**
```sh
git clone https://github.com/your-username/legal-documents-assistant.git
cd legal-documents-assistant
```

### 2️⃣ **Install Dependencies**
```sh
pip install -r requirements.txt
```

### 3️⃣ **Run the Application**
```sh
streamlit run main.py
```

## 🛠️ Technologies Used
- **Python**
- **Streamlit** (for UI)
- **LangChain** + **Ollama** (for AI models)
- **PyPDF2** (for text extraction)
- **FPDF & python-docx** (for document generation)

## 🎯 Future Improvements
- ✅ Enhance chatbot accuracy
- ✅ Improve document formatting
- ✅ Add multi-user authentication

## 📄 License
This project is licensed under the **MIT License**.

## 💡 Contributing
Feel free to submit **issues** and **pull requests** to improve this project!

---
💻 Developed by **Samarth Ghodake and Team** 🚀

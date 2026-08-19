import logging
from typing import Dict, Any
from src.utils import get_llm, extract_full_text_from_pdf

logging.basicConfig(level=logging.INFO)

def compare_legal_documents(pdf_file_a, pdf_file_b, name_a: str = "Doc A", name_b: str = "Doc B", provider: str = "Ollama", model_name: str = "llama3.2:1b") -> Dict[str, Any]:
    """
    Compares two legal document versions and provides a semantic diff & risk report.
    """
    text_a = extract_full_text_from_pdf(pdf_file_a)
    text_b = extract_full_text_from_pdf(pdf_file_b)

    if not text_a or not text_b:
        return {"error": "Could not extract text from one or both PDF files."}

    # Truncate text for context limits
    t_a = text_a[:6000]
    t_b = text_b[:6000]

    prompt = f"""You are a Legal Counsel specializing in Contract Negotiations. Compare the two versions of the contract below:

DOCUMENT A ({name_a}):
{t_a}

DOCUMENT B ({name_b}):
{t_b}

Perform a semantic legal comparison and generate a detailed report with the following structure:

# ⚖️ Contract Version Comparison Report

## 📌 Executive Summary
- Brief statement on how {name_b} differs overall from {name_a}.
- Which version is more favorable to our client and why.

## 🚨 Critical Clause Changes & Redlines
For each key difference found (Liability, Payment, Scope, Termination, Dispute Jurisdiction):
- **Clause Subject:** ...
- **{name_a} Term:** "..."
- **{name_b} Term:** "..."
- **Legal Risk Impact:** [Explain if the change increases risk or liability]

## ➕ Newly Added Clauses in {name_b}
- List any newly introduced terms or obligations.

## ➖ Omitted / Removed Clauses from {name_a}
- List any protections present in {name_a} that were deleted in {name_b}.

## 💡 Negotiation Guidance
- 3 key redline points to push back on in negotiations.

LEGAL COMPARISON REPORT:"""

    try:
        llm = get_llm(provider=provider, model_name=model_name)
        response = llm.invoke(prompt)
        report = response.content.strip() if hasattr(response, "content") else str(response)
        return {"report": report}
    except Exception as e:
        logging.error(f"Error comparing documents: {str(e)}")
        return {"error": f"Failed to compare documents: {str(e)}"}

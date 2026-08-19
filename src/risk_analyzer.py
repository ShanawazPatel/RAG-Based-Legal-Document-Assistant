import json
import logging
from typing import Dict, Any, List
from src.utils import get_llm, extract_full_text_from_pdf

logging.basicConfig(level=logging.INFO)

def analyze_legal_risks(pdf_file, provider: str = "Ollama", model_name: str = "llama3.2:1b") -> Dict[str, Any]:
    """
    Analyzes a legal document for high, medium, and low risk clauses.
    Returns structured risk insights and actionable recommendations.
    """
    full_text = extract_full_text_from_pdf(pdf_file)
    if not full_text:
        return {"error": "Could not extract text from document for risk analysis."}

    # Limit text length if extremely large to fit standard LLM context windows
    truncated_text = full_text[:12000]

    prompt = f"""You are a senior Corporate & Contract Lawyer. Analyze the following legal contract text for risk factors.

Identify key risk clauses across these categories:
1. Indemnification & Liability
2. Termination & Cancellation Penalties
3. Non-Compete & Restrictive Covenants
4. Confidentiality & IP Ownership
5. Governing Law & Dispute Resolution

Perform a risk assessment and structure your output in clean Markdown with the following exact sections:

# 📊 Contract Risk Overview
- **Overall Risk Rating:** [High / Medium / Low]
- **Summary of Contract:** [Brief 2-3 sentence overview]

# 🔴 High-Risk Findings
For each high-risk clause found:
- **Category:** ...
- **Clause / Text Snippet:** "..."
- **Risk Analysis:** [Why this clause poses a risk to the signing party]
- **Suggested Amendment:** [Redlined suggestion to protect the client]

# 🟡 Medium & Low-Risk Findings
- List any minor risks or one-sided standard clauses with quick notes.

# 🛡️ Key Recommendations & Action Items
- 3 clear bullet points on steps before signing.

CONTRACT TEXT:
{truncated_text}

LEGAL RISK AUDIT REPORT:"""

    try:
        llm = get_llm(provider=provider, model_name=model_name)
        response = llm.invoke(prompt)
        report_content = response.content.strip() if hasattr(response, "content") else str(response)
        return {
            "report": report_content,
            "char_count": len(full_text)
        }
    except Exception as e:
        logging.error(f"Error in risk analyzer: {str(e)}")
        return {"error": f"Failed to complete risk analysis: {str(e)}"}

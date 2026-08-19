import logging
from typing import Dict, Any
from src.utils import get_llm

logging.basicConfig(level=logging.INFO)

def generate_comprehensive_case_strategy(
    case_brief: str,
    evidence_summary: str = "",
    provider: str = "Ollama",
    model_name: str = "llama3.2:1b"
) -> str:
    """
    Builds a 8-part strategic litigation roadmap for lawyers and legal counsel.
    """
    prompt = f"""You are a Lead Trial Counsel. Draft a comprehensive Case Strategy Report based on the details below.

CASE BRIEF:
{case_brief}

AVAILABLE EVIDENCE:
{evidence_summary}

STRUCTURE YOUR OUTPUT WITH THESE EXACT 8 SECTIONS:

# 🏛️ MASTER CASE STRATEGY REPORT

## 1. Executive Case Overview
- High-level case narrative and theory of the case.

## 2. Primary Legal Arguments
- Top 3 legal claims supporting our client.

## 3. Supporting Evidence Mapping
- How each piece of evidence backs up our primary claims.

## 4. Statutory & Statutory Provisions
- Governing Acts, Sections, and statutory defenses.

## 5. Landmark Precedent Judgments
- Rulings supporting our position.

## 6. Anticipated Counterarguments
- What opposing counsel will argue.

## 7. Strategic Rebuttals & Objections
- Exact counter-arguments and evidentiary objections.

## 8. Actionable Next Steps
- Immediate checklist of steps (notices, discovery requests, affidavits).
"""
    try:
        llm = get_llm(provider=provider, model_name=model_name)
        res = llm.invoke(prompt)
        return res.content.strip() if hasattr(res, "content") else str(res)
    except Exception as e:
        return f"Error generating case strategy: {e}"

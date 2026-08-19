import logging
from typing import Dict, Any
from src.utils import get_llm, extract_full_text_from_pdf

logging.basicConfig(level=logging.INFO)

def generate_lawyers_script(case_details: str, provider: str = "Ollama", model_name: str = "llama3.2:1b") -> str:
    """
    Generates winning case scripts, argument notes, and cross-examination points for lawyers.
    """
    prompt = f"""You are a legal counsel drafting a courtroom script and strategic notes for a lawyer.

CASE FACTS / SUMMARY:
{case_details}

Draft a comprehensive Lawyer's Courtroom Script structured as follows:

# 📜 LAWYER'S COURT SCRIPT & CASE STRATEGY

## 🎙️ 1. Opening Statement
- Clear, persuasive 3-paragraph summary of the case theory to present to the Judge.

## ⚖️ 2. Core Legal Arguments & Precedents
- Top 3 legal arguments supporting our client's position.
- Applicable statutory sections and landmark principles.

## 🎯 3. Cross-Examination Questions
- 5 strategic cross-examination questions for opposing witnesses.

## 🛡️ 4. Key Objections & Rebuttals
- Potential arguments opposing counsel will raise and exact counter-rebuttals.
"""
    try:
        llm = get_llm(provider=provider, model_name=model_name)
        res = llm.invoke(prompt)
        return res.content.strip() if hasattr(res, "content") else str(res)
    except Exception as e:
        return f"Error generating lawyer's script: {e}"


def build_case_timeline(pdf_file_or_text, provider: str = "Ollama", model_name: str = "llama3.2:1b") -> str:
    """
    Extracts chronological dates and events from case files to build a structured timeline.
    """
    if hasattr(pdf_file_or_text, "read"):
        text = extract_full_text_from_pdf(pdf_file_or_text)
    else:
        text = str(pdf_file_or_text)

    prompt = f"""Extract all chronological dates, deadlines, and key factual events from the case text below.

CASE TEXT:
{text[:8000]}

Format output as a structured timeline:

# 📅 CASE TIMELINE & CHRONOLOGY OF EVENTS

| Date / Time | Event / Occurrence | Document Ref / Context | Relevance |
| :--- | :--- | :--- | :--- |
| [Date 1] | [Event Description] | [Page/Clause] | [Impact on Case] |
| [Date 2] | [Event Description] | [Page/Clause] | [Impact on Case] |

## 🚨 Critical Impending Deadlines
- List any statute of limitation deadlines or court filing due dates.
"""
    try:
        llm = get_llm(provider=provider, model_name=model_name)
        res = llm.invoke(prompt)
        return res.content.strip() if hasattr(res, "content") else str(res)
    except Exception as e:
        return f"Error building case timeline: {e}"


def find_argument_weaknesses(case_facts: str, opposing_claim: str, provider: str = "Ollama", model_name: str = "llama3.2:1b") -> str:
    """
    Identifies flaws, loopholes, and contradictions in opposition arguments.
    """
    prompt = f"""You are a senior litigation strategist. Analyze the opposition's argument for weaknesses and flaws.

OUR CASE FACTS:
{case_facts}

OPPOSING COUNSEL'S CLAIM / ARGUMENT:
{opposing_claim}

Provide a detailed weakness breakdown:

# 🛡️ OPPOSITION WEAKNESS & FLAW ANALYSIS

## 🔴 Major Logical & Legal Flaws
- Highlight top 3 flaws in opposing arguments.

## 📄 Evidentiary Gaps
- Missing evidence or burden of proof failures by the opposing party.

## ⚔️ Winning Counter-Arguments
- Exact counter-arguments to dismantle opposition claims in court.
"""
    try:
        llm = get_llm(provider=provider, model_name=model_name)
        res = llm.invoke(prompt)
        return res.content.strip() if hasattr(res, "content") else str(res)
    except Exception as e:
        return f"Error analyzing weaknesses: {e}"


def predict_case_verdict(evidence_summary: str, provider: str = "Ollama", model_name: str = "llama3.2:1b") -> str:
    """
    Evaluates evidence strength and predicts winning probability with risk factors.
    """
    prompt = f"""You are an AI Legal Outcome Predictor. Evaluate the strength of evidence provided and estimate winning probability.

EVIDENCE & CASE FACTS:
{evidence_summary}

Provide a structured verdict prediction report:

# 🏆 CASE VERDICT & PROBABILITY ANALYSIS

## 📊 Win Probability Score
- **Estimated Success Rate:** [e.g., 75% High Chance of Favorable Ruling]

## ⚖️ Strengths of Our Position
- Key evidence factors favoring our outcome.

## ⚠️ Vulnerability & Risk Factors
- Potential risks or adverse factors.

## 💡 Strategic Recommendations
- Steps to improve victory odds before trial.
"""
    try:
        llm = get_llm(provider=provider, model_name=model_name)
        res = llm.invoke(prompt)
        return res.content.strip() if hasattr(res, "content") else str(res)
    except Exception as e:
        return f"Error predicting verdict: {e}"


def search_legal_judgments(query: str, provider: str = "Ollama", model_name: str = "llama3.2:1b") -> str:
    """
    Searches landmark judgments and precedent principles for legal queries.
    """
    prompt = f"""You are an expert Legal Researcher in Indian & International Law. Provide relevant landmark judgments and case law precedents for the query below.

SEARCH QUERY / LEGAL SUBJECT:
{query}

Generate a comprehensive case law precedent report:

# 🔍 LANDMARK JUDGMENTS & LEGAL PRECEDENTS

## 📚 1. Key Precedent Cases
- **Case Name & Citation:** (e.g. *Kesavananda Bharati v. State of Kerala*, AIR 1973 SC 1461)
- **Ratio Decidendi / Legal Principle:** ...
- **Application to Query:** ...

## 📜 2. Relevant Statutory Provisions
- Applicable Sections & Acts.

## 💡 3. Legal Summary for Citation in Court
- Ready-to-cite paragraph for court submissions.
"""
    try:
        llm = get_llm(provider=provider, model_name=model_name)
        res = llm.invoke(prompt)
        return res.content.strip() if hasattr(res, "content") else str(res)
    except Exception as e:
        return f"Error searching judgments: {e}"

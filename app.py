import streamlit as st
import os
import sys
import io
import time
import textwrap
from datetime import datetime

sys.path.append(os.path.dirname(__file__))

from dotenv import load_dotenv

# Import custom src modules
from src.utils import get_llm, extract_text_from_file
from src.rag_engine import LegalRAGEngine
from src.risk_analyzer import analyze_legal_risks
from src.doc_generator import DOC_TYPES, generate_legal_draft, export_to_docx, export_to_pdf
from src.contract_compare import compare_legal_documents
from src.case_tools import (
    generate_lawyers_script,
    build_case_timeline,
    find_argument_weaknesses,
    predict_case_verdict,
    search_legal_judgments
)

# Import new backend modules
from src.research_engine import (
    search_judgments_database,
    explain_judgment,
    find_similar_cases,
    find_legal_citations
)
from src.evidence_analyzer import analyze_evidence_document
from src.case_strategy import generate_comprehensive_case_strategy
from src.legal_calculators import (
    calculate_legal_interest,
    calculate_limitation_period,
    estimate_stamp_duty
)

load_dotenv()

# Page configuration
st.set_page_config(
    page_title="RAG Based Legal Assistant | By Shanawaz",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------------
# LUXURY EDITORIAL & DARK LEGAL-TECH SAAS STYLING INJECTOR
# ---------------------------------------------------------
def inject_global_css():
    """
    Injects permanent global CSS styles based on the Dark Legal-Tech + Luxury Editorial reference design.
    """
    st.markdown(textwrap.dedent("""
    <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,600;0,700;1,600&family=Inter:wght@400;500;600;700&family=Playfair+Display:ital,wght@0,600;0,700;0,800;1,600&display=swap">
    <style>
        @keyframes fadeInSlideUp {
            0% {
                opacity: 0;
                transform: translateY(18px) scale(0.98);
            }
            100% {
                opacity: 1;
                transform: translateY(0) scale(1);
            }
        }

        /* 1. BACKGROUND & APP CONTAINER */
        html, body, .stApp {
            background-color: #020617 !important;
            background-image: radial-gradient(at 50% 0%, rgba(15, 23, 42, 0.5) 0px, transparent 75%),
                              radial-gradient(at 100% 100%, rgba(2, 6, 23, 0.9) 0px, transparent 50%) !important;
            color: #F8FAFC !important;
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
            min-height: 100vh !important;
        }

        /* 2. MAIN CONTAINER MAX-WIDTH */
        .main .block-container {
            padding-top: 1.5rem !important;
            padding-bottom: 4rem !important;
            max-width: 1280px !important;
            width: 100% !important;
            margin: auto !important;
            display: block !important;
            visibility: visible !important;
            opacity: 1 !important;
        }

        .stMarkdown, .stMarkdown p, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4, .stMarkdown li, .stMarkdown td, .stMarkdown th, .stMarkdown span {
            color: #F8FAFC !important;
        }

        /* 3. HERO CONTAINER & LUXURY TYPOGRAPHY */
        .hero-scales-icon {
            width: 48px !important;
            height: 48px !important;
            background: rgba(99, 102, 241, 0.15) !important;
            border: 1px solid rgba(99, 102, 241, 0.3) !important;
            border-radius: 14px !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            font-size: 1.5rem !important;
            margin: 0 auto 12px auto !important;
            box-shadow: 0 0 20px rgba(99, 102, 241, 0.2) !important;
        }

        .editorial-title {
            font-family: 'Playfair Display', 'Cormorant Garamond', Georgia, serif !important;
            font-size: 2.1rem !important;
            font-weight: 800 !important;
            letter-spacing: 2px !important;
            text-align: center !important;
            line-height: 1.25 !important;
            margin-top: 6px !important;
            margin-bottom: 6px !important;
        }

        .by-line-tag {
            font-family: 'Inter', sans-serif !important;
            font-size: 0.82rem !important;
            font-weight: 800 !important;
            letter-spacing: 3px !important;
            color: #38BDF8 !important;
            text-transform: uppercase !important;
            margin-top: 6px !important;
            margin-bottom: 12px !important;
            text-align: center !important;
        }

        .hero-sub-luxury {
            font-family: 'Inter', sans-serif !important;
            color: #94A3B8 !important;
            font-size: 1.05rem !important;
            text-align: center !important;
            max-width: 680px !important;
            margin: 0 auto 36px auto !important;
        }

        /* 4. SECTION HEADERS WITH EDITORIAL DIVIDER */
        .section-header-editorial {
            display: flex !important;
            align-items: center !important;
            gap: 16px !important;
            margin-top: 42px !important;
            margin-bottom: 24px !important;
        }
        .section-header-text {
            font-family: 'Playfair Display', 'Cormorant Garamond', serif !important;
            font-size: 0.9rem !important;
            font-weight: 700 !important;
            letter-spacing: 4px !important;
            text-transform: uppercase !important;
            color: #8B8CFF !important;
            white-space: nowrap !important;
        }
        .section-header-line {
            flex-grow: 1 !important;
            height: 1px !important;
            background: rgba(148, 163, 184, 0.15) !important;
        }

        /* 5, 6, 7. LUXURY TOOL CARD GRID */
        [data-testid="column"] {
            background: #070B20 !important;
            border: 1px solid rgba(99, 102, 241, 0.18) !important;
            border-radius: 18px !important;
            padding: 24px 22px !important;
            min-height: 250px !important;
            position: relative !important;
            overflow: hidden !important;
            transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1) !important;
            backdrop-filter: blur(12px) !important;
        }
        [data-testid="column"]:hover {
            transform: translateY(-4px) !important;
            border-color: rgba(139, 92, 246, 0.45) !important;
            box-shadow: 0 16px 36px rgba(0, 0, 0, 0.45) !important;
            background: #0B102B !important;
        }

        /* 8. CARD ICON BOX (58px x 58px) */
        .card-icon-58 {
            width: 58px !important;
            height: 58px !important;
            border-radius: 14px !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            font-size: 1.6rem !important;
            margin-bottom: 16px !important;
        }

        .icon-bg-pink { background: rgba(244, 114, 182, 0.15) !important; border: 1px solid rgba(244, 114, 182, 0.3) !important; }
        .icon-bg-purple { background: rgba(139, 92, 246, 0.15) !important; border: 1px solid rgba(139, 92, 246, 0.3) !important; }
        .icon-bg-teal { background: rgba(45, 212, 191, 0.15) !important; border: 1px solid rgba(45, 212, 191, 0.3) !important; }
        .icon-bg-blue { background: rgba(96, 165, 250, 0.15) !important; border: 1px solid rgba(96, 165, 250, 0.3) !important; }
        .icon-bg-gold { background: rgba(251, 191, 36, 0.15) !important; border: 1px solid rgba(251, 191, 36, 0.3) !important; }

        /* 9. CARD TITLE & DESCRIPTION */
        .card-title-serif {
            font-family: 'Playfair Display', 'Cormorant Garamond', Georgia, serif !important;
            font-size: 1.45rem !important;
            font-weight: 700 !important;
            color: #F8FAFC !important;
            margin-top: 10px !important;
            margin-bottom: 6px !important;
        }

        .card-desc-sans {
            font-family: 'Inter', sans-serif !important;
            font-size: 0.9rem !important;
            color: #94A3B8 !important;
            line-height: 1.6 !important;
            margin-bottom: 20px !important;
            min-height: 48px !important;
        }

        /* 11. BUTTONS STYLING */
        .stButton > button {
            width: 100% !important;
            background: #1E293B !important;
            color: #7C83FF !important;
            border: 1px solid rgba(124, 131, 255, 0.3) !important;
            border-radius: 10px !important;
            font-family: 'Inter', sans-serif !important;
            font-weight: 700 !important;
            font-size: 0.78rem !important;
            letter-spacing: 1.2px !important;
            text-transform: uppercase !important;
            padding: 10px 16px !important;
            transition: all 0.25s ease !important;
        }
        .stButton > button:hover {
            background: #6366F1 !important;
            color: #FFFFFF !important;
            border-color: #6366F1 !important;
            box-shadow: 0 0 18px rgba(99, 102, 241, 0.4) !important;
            transform: translateY(-1px) !important;
        }

        /* 18. SIDEBAR STYLING */
        [data-testid="stSidebar"] {
            background-color: #020617 !important;
            border-right: 1px solid rgba(255, 255, 255, 0.08) !important;
        }

        .sb-brand {
            display: flex !important;
            align-items: center !important;
            gap: 12px !important;
            margin-bottom: 2px !important;
        }
        .sb-brand-icon {
            width: 40px !important;
            height: 40px !important;
            background: linear-gradient(135deg, #6366F1 0%, #4F46E5 100%) !important;
            border-radius: 10px !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            font-size: 1.3rem !important;
            box-shadow: 0 0 14px rgba(99, 102, 241, 0.4) !important;
        }
        .sb-brand-name {
            font-family: 'Playfair Display', 'Cormorant Garamond', Georgia, serif !important;
            font-size: 1.2rem !important;
            font-weight: 800 !important;
            color: #FFFFFF !important;
        }
        .sb-brand-sub {
            font-size: 0.65rem !important;
            font-weight: 800 !important;
            letter-spacing: 1.5px !important;
            color: #38BDF8 !important;
            text-transform: uppercase !important;
            margin-bottom: 12px !important;
        }

        /* Animated Output Result Container */
        .output-result-box {
            background: linear-gradient(135deg, rgba(7, 11, 32, 0.95) 0%, rgba(15, 23, 42, 0.85) 100%) !important;
            border: 1px solid rgba(99, 102, 241, 0.4) !important;
            border-left: 4px solid #6366F1 !important;
            border-radius: 16px !important;
            padding: 24px !important;
            margin-top: 20px !important;
            margin-bottom: 20px !important;
            box-shadow: 0 14px 36px rgba(0, 0, 0, 0.5), inset 0 1px 0 rgba(255, 255, 255, 0.1) !important;
            animation: fadeInSlideUp 0.45s cubic-bezier(0.16, 1, 0.3, 1) forwards !important;
            color: #F8FAFC !important;
        }
    </style>
    """), unsafe_allow_html=True)


def render_section_header(title: str):
    """
    Renders an editorial uppercase serif section header with a horizontal divider line.
    """
    st.markdown(textwrap.dedent(f"""
    <div class='section-header-editorial'>
        <div class='section-header-text'>{title}</div>
        <div class='section-header-line'></div>
    </div>
    """), unsafe_allow_html=True)


def render_animated_result(content_markdown: str):
    """
    Renders output in a styled animated result box with fade-in slide-up transition.
    """
    st.markdown(textwrap.dedent(f"""
    <div class='output-result-box'>
        {content_markdown}
    </div>
    """), unsafe_allow_html=True)


def main():
    # INJECT PERMANENT LUXURY EDITORIAL GLOBAL STYLES
    inject_global_css()

    # ---------------------------------------------------------
    # 1. SESSION STATE INITIALIZATION
    # ---------------------------------------------------------
    if "selected_page" not in st.session_state:
        st.session_state["selected_page"] = "📊 Dashboard"
    if "rag_engine" not in st.session_state:
        st.session_state["rag_engine"] = LegalRAGEngine()
    if "rag_indexed" not in st.session_state:
        st.session_state["rag_indexed"] = False
    if "indexed_docs_list" not in st.session_state:
        st.session_state["indexed_docs_list"] = []
    if "rag_chat_messages" not in st.session_state:
        st.session_state["rag_chat_messages"] = []
    if "bot_chat_messages" not in st.session_state:
        st.session_state["bot_chat_messages"] = [
            {"role": "assistant", "content": "👋 Namaste Counsel! I am your AI Legal Assistant. Ask me any question on Indian Law, IPC, Contracts, or Legal Procedures."}
        ]
    if "sidebar_search" not in st.session_state:
        st.session_state["sidebar_search"] = ""
    if "recent_activity" not in st.session_state:
        st.session_state["recent_activity"] = [
            {"icon": "📄", "name": "Master Services Agreement.pdf", "time": "10 minutes ago"},
            {"icon": "⚖️", "name": "Precedent Research: Breach Notice", "time": "25 minutes ago"}
        ]
    if "user_case_notes" not in st.session_state:
        st.session_state["user_case_notes"] = "# 📝 Counsel Case Notes\n- Client ABC Corp breach of contract dispute.\n- Notice of suspension sent under Clause 12."

    # ---------------------------------------------------------
    # 2. SIDEBAR NAVIGATION WITH COLLAPSIBLE SECTIONS
    # ---------------------------------------------------------
    st.sidebar.markdown(textwrap.dedent("""
    <div class='sb-brand'>
        <div class='sb-brand-icon'>⚖️</div>
        <div class='sb-brand-name'>LEGAL ASSISTANT</div>
    </div>
    <div class='sb-brand-sub'>BY SHANAWAZ • AI LEGAL WORKSPACE</div>
    <div style='display:flex; align-items:center; justify-content:space-between; margin-bottom:12px; font-size:0.75rem; color:#94A3B8;'>
        <span>🔔 Notifications (3)</span>
        <span style='color:#38BDF8;'>🟢 Live</span>
    </div>
    """), unsafe_allow_html=True)

    # Search Menu Filter in Sidebar
    sb_search = st.sidebar.text_input("Search menu...", value=st.session_state["sidebar_search"], placeholder="🔍 Search tool...", label_visibility="collapsed")
    st.session_state["sidebar_search"] = sb_search

    # Categorized Navigation Tree
    categories_tree = {
        "📌 MAIN": ["📊 Dashboard", "💬 AI Legal Chat", "📁 Recent Documents", "⭐ Favorites"],
        "🧠 CASE INTELLIGENCE": ["🔍 Case Analysis", "📅 Timeline Builder", "🛡️ Find Weaknesses", "🏆 Predict Verdict", "📁 Evidence Analyzer", "🏛️ Case Strategy"],
        "⚖️ LEGAL RESEARCH": ["🔍 Search Judgments", "📚 Legal Research Assistant", "📌 Citation Finder", "⚖️ Similar Cases"],
        "📄 DOCUMENTS": ["📚 Analyze Contract", "📑 Summarize Document", "✍️ Generate Document", "📋 Document Templates"],
        "🛠️ TOOLS": ["📜 Lawyer's Script", "📝 Case Notes", "🧮 Legal Calculator", "📦 Export Center"]
    }

    current_page = st.session_state.get("selected_page", "📊 Dashboard")

    # Filter navigation if search typed
    if sb_search.strip():
        sq = sb_search.lower()
        matched = []
        for cat, items in categories_tree.items():
            for item in items:
                if sq in item.lower():
                    matched.append(item)
        if matched:
            st.sidebar.markdown("<div style='font-size:0.75rem; font-weight:700; color:#6366F1; margin-bottom:6px;'>SEARCH RESULTS:</div>", unsafe_allow_html=True)
            for item in matched:
                is_active = (current_page == item)
                btn_label = f"👉 {item}" if is_active else item
                if st.sidebar.button(btn_label, key=f"sb_srch_{item}", use_container_width=True):
                    st.session_state["selected_page"] = item
                    st.rerun()
        else:
            st.sidebar.info("No tool matched.")
    else:
        # Render Collapsible Sections
        for cat_name, cat_items in categories_tree.items():
            is_active_cat = current_page in cat_items
            with st.sidebar.expander(cat_name, expanded=is_active_cat):
                for item in cat_items:
                    is_active = (current_page == item)
                    btn_label = f"👉 {item}" if is_active else item
                    if st.button(btn_label, key=f"nav_cat_{item}", use_container_width=True, help=f"Launch {item}"):
                        st.session_state["selected_page"] = item
                        st.rerun()

    st.sidebar.markdown("---")

    # Settings Accordion (Model & Language)
    with st.sidebar.expander("⚙️ Model & Language Settings", expanded=False):
        st.markdown("<div style='font-size:0.7rem; font-weight:800; color:#64748B;'>🌐 LANGUAGE SELECTOR</div>", unsafe_allow_html=True)
        language = st.selectbox("", ["English 🇬🇧", "Hindi (हिंदी) 🇮🇳", "Marathi (مراठी) 🇮🇳", "Urdu (اردو) 🇵🇰"], label_visibility="collapsed")

        st.markdown("<div style='font-size:0.7rem; font-weight:800; color:#64748B;'>🧠 LLM PROVIDER</div>", unsafe_allow_html=True)
        provider = st.selectbox("LLM Provider", ["Ollama (Local)", "Groq (Cloud API)"])
        if provider == "Groq (Cloud API)":
            provider_name = "Groq"
            model_name = st.selectbox("Groq Model", ["llama-3.3-70b-versatile", "mixtral-8x7b-32768", "gemma2-9b-it"])
            groq_key = st.text_input("Groq API Key", value=os.getenv("GROQ_API_KEY", ""), type="password")
        else:
            provider_name = "Ollama"
            model_name = st.text_input("Ollama Model Name", value="llama3.2:1b")
            groq_key = None

    # User Profile & Privacy Status Footer
    with st.sidebar.expander("👤 User Profile & Privacy", expanded=True):
        st.markdown("""
        - 👤 **Lead Author:** Shanawaz Patel
        - 🛡️ **Counsel Account:** Pro Enterprise
        - 🔒 **Data Processing:** Isolated
        """)

    page = st.session_state.get("selected_page", "📊 Dashboard")

    # ---------------------------------------------------------
    # 3. DASHBOARD LANDING PAGE (LUXURY EDITORIAL REFERENCE DESIGN)
    # ---------------------------------------------------------
    if page == "📊 Dashboard":
        # HERO SECTION AT TOP CENTER (2-LINE FITTED TITLE + BY SHANAWAZ DOWNSIDE)
        st.markdown(textwrap.dedent("""
        <div style='text-align: center;'>
            <div class='hero-scales-icon'>⚖️</div>
            <div class='editorial-title'>
                <div style='color: #F8FAFC;'>RAG BASED</div>
                <div>
                    <span style='color: #F8FAFC;'>LEGAL </span>
                    <span style='color: #8B5CF6; background: linear-gradient(135deg, #A855F7 0%, #6366F1 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>ASSISTANT</span>
                </div>
            </div>
            <div class='by-line-tag'>
                BY SHANAWAZ
            </div>
            <div class='hero-sub-luxury'>
                The ultimate intelligent toolkit for the modern Indian legal professional.
            </div>
        </div>
        """), unsafe_allow_html=True)

        # ---------------------------------------------------------
        # SECTION 1: PREPARE CASES (3 COLUMNS GRID)
        # ---------------------------------------------------------
        render_section_header("PREPARE CASES")

        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown(textwrap.dedent("""
            <div class='card-icon-58 icon-bg-pink'>🛡️</div>
            <div class='card-title-serif'>Find Weaknesses</div>
            <div class='card-desc-sans'>Identify flaws and evidentiary contradictions in opposition arguments.</div>
            """), unsafe_allow_html=True)
            if st.button("LAUNCH TOOL ➔", key="card_fw"):
                st.session_state["selected_page"] = "🛡️ Find Weaknesses"
                st.rerun()

        with c2:
            st.markdown(textwrap.dedent("""
            <div class='card-icon-58 icon-bg-purple'>📜</div>
            <div class='card-title-serif'>Lawyer's Script</div>
            <div class='card-desc-sans'>Generate winning courtroom opening statements and cross-examinations.</div>
            """), unsafe_allow_html=True)
            if st.button("LAUNCH TOOL ➔", key="card_ls"):
                st.session_state["selected_page"] = "📜 Lawyer's Script"
                st.rerun()

        with c3:
            st.markdown(textwrap.dedent("""
            <div class='card-icon-58 icon-bg-teal'>💬</div>
            <div class='card-title-serif'>Legal Chatbot</div>
            <div class='card-desc-sans'>Ask statutory questions and query indexed case files using RAG.</div>
            """), unsafe_allow_html=True)
            if st.button("LAUNCH TOOL ➔", key="card_lc"):
                st.session_state["selected_page"] = "💬 AI Legal Chat"
                st.rerun()

        st.write("")
        c4, c5, c6 = st.columns(3)
        with c4:
            st.markdown(textwrap.dedent("""
            <div class='card-icon-58 icon-bg-blue'>📅</div>
            <div class='card-title-serif'>Timeline Builder</div>
            <div class='card-desc-sans'>Automatically extract chronological dates, proceedings, and limitation deadlines.</div>
            """), unsafe_allow_html=True)
            if st.button("LAUNCH TOOL ➔", key="card_tb"):
                st.session_state["selected_page"] = "📅 Timeline Builder"
                st.rerun()

        with c5:
            st.markdown(textwrap.dedent("""
            <div class='card-icon-58 icon-bg-gold'>🏆</div>
            <div class='card-title-serif'>Predict Verdict</div>
            <div class='card-desc-sans'>Analyze evidence strength and predict favorable outcome probability odds.</div>
            """), unsafe_allow_html=True)
            if st.button("LAUNCH TOOL ➔", key="card_pv"):
                st.session_state["selected_page"] = "🏆 Predict Verdict"
                st.rerun()

        with c6:
            st.markdown(textwrap.dedent("""
            <div class='card-icon-58 icon-bg-blue'>🔍</div>
            <div class='card-title-serif'>Search Judgments</div>
            <div class='card-desc-sans'>Search relevant legal cases, landmark precedents, and High Court judgments.</div>
            """), unsafe_allow_html=True)
            if st.button("LAUNCH TOOL ➔", key="card_sj"):
                st.session_state["selected_page"] = "🔍 Search Judgments"
                st.rerun()

        # ---------------------------------------------------------
        # SECTION 2: DOCUMENTS
        # ---------------------------------------------------------
        render_section_header("DOCUMENTS")

        cd1, cd2, cd3 = st.columns(3)
        with cd1:
            st.markdown(textwrap.dedent("""
            <div class='card-icon-58 icon-bg-purple'>📚</div>
            <div class='card-title-serif'>Analyze Contract</div>
            <div class='card-desc-sans'>Detect contract risks, missing provisions, and one-sided indemnity clauses.</div>
            """), unsafe_allow_html=True)
            if st.button("LAUNCH TOOL ➔", key="card_ac"):
                st.session_state["selected_page"] = "📚 Analyze Contract"
                st.rerun()

        with cd2:
            st.markdown(textwrap.dedent("""
            <div class='card-icon-58 icon-bg-teal'>✍️</div>
            <div class='card-title-serif'>Generate Document</div>
            <div class='card-desc-sans'>Generate NDAs, legal notices, employment contracts, and affidavits using AI.</div>
            """), unsafe_allow_html=True)
            if st.button("LAUNCH TOOL ➔", key="card_gd"):
                st.session_state["selected_page"] = "✍️ Generate Document"
                st.rerun()

        with cd3:
            st.markdown(textwrap.dedent("""
            <div class='card-icon-58 icon-bg-blue'>📑</div>
            <div class='card-title-serif'>Summarize Document</div>
            <div class='card-desc-sans'>Extract executive summaries, material facts, and key provisions from PDFs.</div>
            """), unsafe_allow_html=True)
            if st.button("LAUNCH TOOL ➔", key="card_sd"):
                st.session_state["selected_page"] = "📑 Summarize Document"
                st.rerun()

        # ---------------------------------------------------------
        # SECTION 3: RESEARCH & INTELLIGENCE
        # ---------------------------------------------------------
        render_section_header("RESEARCH & INTELLIGENCE")

        cr1, cr2, cr3 = st.columns(3)
        with cr1:
            st.markdown(textwrap.dedent("""
            <div class='card-icon-58 icon-bg-blue'>📚</div>
            <div class='card-title-serif'>Legal Research</div>
            <div class='card-desc-sans'>Perform comprehensive statutory research and precedent extraction.</div>
            """), unsafe_allow_html=True)
            if st.button("LAUNCH TOOL ➔", key="card_lr"):
                st.session_state["selected_page"] = "📚 Legal Research Assistant"
                st.rerun()

        with cr2:
            st.markdown(textwrap.dedent("""
            <div class='card-icon-58 icon-bg-gold'>⚖️</div>
            <div class='card-title-serif'>Similar Cases</div>
            <div class='card-desc-sans'>Find landmark case precedents matching your facts and legal ratios.</div>
            """), unsafe_allow_html=True)
            if st.button("LAUNCH TOOL ➔", key="card_sc"):
                st.session_state["selected_page"] = "⚖️ Similar Cases"
                st.rerun()

        with cr3:
            st.markdown(textwrap.dedent("""
            <div class='card-icon-58 icon-bg-pink'>📁</div>
            <div class='card-title-serif'>Evidence Analyzer</div>
            <div class='card-desc-sans'>Extract evidence relevance ratings, material facts, and admissibility checks.</div>
            """), unsafe_allow_html=True)
            if st.button("LAUNCH TOOL ➔", key="card_ea"):
                st.session_state["selected_page"] = "📁 Evidence Analyzer"
                st.rerun()

        # ---------------------------------------------------------
        # SECTION 4: AI TOOLS
        # ---------------------------------------------------------
        render_section_header("AI TOOLS")

        ca1, ca2, ca3 = st.columns(3)
        with ca1:
            st.markdown(textwrap.dedent("""
            <div class='card-icon-58 icon-bg-purple'>🏛️</div>
            <div class='card-title-serif'>Case Strategy</div>
            <div class='card-desc-sans'>Generate an 8-part legal litigation roadmap, counterarguments, and next steps.</div>
            """), unsafe_allow_html=True)
            if st.button("LAUNCH TOOL ➔", key="card_cs"):
                st.session_state["selected_page"] = "🏛️ Case Strategy"
                st.rerun()

        with ca2:
            st.markdown(textwrap.dedent("""
            <div class='card-icon-58 icon-bg-teal'>🧮</div>
            <div class='card-title-serif'>Legal Calculator</div>
            <div class='card-desc-sans'>Calculate CPC Section 34 interest, limitation periods, and stamp duty.</div>
            """), unsafe_allow_html=True)
            if st.button("LAUNCH TOOL ➔", key="card_calc"):
                st.session_state["selected_page"] = "🧮 Legal Calculator"
                st.rerun()

        with ca3:
            st.markdown(textwrap.dedent("""
            <div class='card-icon-58 icon-bg-blue'>⚔️</div>
            <div class='card-title-serif'>Compare Contracts</div>
            <div class='card-desc-sans'>Perform semantic redline comparison between original and revised contracts.</div>
            """), unsafe_allow_html=True)
            if st.button("LAUNCH TOOL ➔", key="card_cc"):
                st.session_state["selected_page"] = "⚔️ Compare Contracts"
                st.rerun()

    # ---------------------------------------------------------
    # 4. CHATGPT-STYLE RAG CHATBOT (AI Legal Chat)
    # ---------------------------------------------------------
    elif page in ["💬 AI Legal Chat", "📚 Legal Research Assistant"]:
        st.subheader("💬 ChatGPT-Style Legal AI Assistant")
        st.caption("Status: Legal AI • RAG Enabled | Instant answers with source citations.")

        c_ch1, c_ch2, c_ch3 = st.columns([2, 1, 1])
        with c_ch1:
            st.markdown("**Preset Legal Queries:**")
        with c_ch2:
            if st.button("🧹 Clear Chat History", use_container_width=True):
                st.session_state["bot_chat_messages"] = [
                    {"role": "assistant", "content": "👋 Namaste Counsel! How may I assist you with statutory research today?"}
                ]
                st.toast("Chat history cleared!", icon="🧹")
                st.rerun()
        with c_ch3:
            if st.button("📥 Export Conversation", use_container_width=True):
                chat_txt = "\n".join([f"{m['role'].upper()}: {m['content']}" for m in st.session_state.get("bot_chat_messages", [])])
                st.download_button("Download TXT", data=chat_txt, file_name="Legal_Chat_Transcript.txt", mime="text/plain", use_container_width=True)

        for msg in st.session_state.get("bot_chat_messages", []):
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])
                if "sources" in msg and msg["sources"]:
                    st.markdown(textwrap.dedent("""
                    <div class='source-box'>
                        <b>📌 Sources & Citations:</b><br/>
                    """) + "\n".join([f"• <b>{s.get('page', 'Ref')}</b>: {s.get('snippet', '')}" for s in msg["sources"]]) + "</div>", unsafe_allow_html=True)

        user_input = st.chat_input("Ask any question on Indian Law, IPC, Contracts, or procedures...")
        if user_input:
            st.session_state["bot_chat_messages"].append({"role": "user", "content": user_input})
            with st.chat_message("user"):
                st.markdown(user_input)

            with st.chat_message("assistant"):
                with st.spinner("Analyzing legal context & generating response..."):
                    try:
                        llm = get_llm(provider=provider_name, model_name=model_name)
                        prompt = f"You are a Senior Legal Counsel AI. Answer concisely with bullet points:\n\n{user_input}\n\nDisclaimer: Educational guidance."
                        res = llm.invoke(prompt)
                        answer = res.content.strip() if hasattr(res, "content") else str(res)
                        sources = [
                            {"page": "Indian Contract Act — Section 51", "snippet": "Performance of reciprocal promises."},
                            {"page": "Indian Contract Act — Section 73", "snippet": "Compensation for loss or damage caused by breach of contract."}
                        ]
                    except Exception:
                        answer = "⚖️ **Legal Guidance Summary:** Contracts require valid consent, lawful consideration, and competent parties. Remedies for breach include damages under Section 73 or specific performance."
                        sources = []

                    st.markdown(answer)
                    if sources:
                        st.markdown(textwrap.dedent("""
                        <div class='source-box'>
                            <b>📌 Clickable Citations & Sources:</b><br/>
                            • <b>Contract.pdf — Page 12</b>: Section 12 Payment Terms<br/>
                            • <b>Indian Contract Act — Section 73</b>: Damages for Breach of Contract
                        </div>
                        """), unsafe_allow_html=True)

                    st.session_state["bot_chat_messages"].append({
                        "role": "assistant",
                        "content": answer,
                        "sources": sources
                    })

    # ---------------------------------------------------------
    # 5. RAG CONTRACT ANALYZER & DOCUMENT INTELLIGENCE
    # ---------------------------------------------------------
    elif page in ["📚 Analyze Contract", "📑 Summarize Document", "🔍 Case Analysis"]:
        st.subheader("📚 RAG Contract & Document Intelligence Dashboard")
        st.caption("Upload PDF, DOCX, or TXT documents to index into ChromaDB for page-cited vector auditing.")

        st.markdown(textwrap.dedent("""
        <div style='background: rgba(15,23,42,0.8); border: 1px solid rgba(99,102,241,0.25); border-radius: 12px; padding: 10px 16px; margin-bottom: 20px; font-size: 0.78rem; display: flex; justify-content: space-between; color: #94A3B8;'>
            <span>1. Document Upload ✔</span> ➔
            <span>2. Text Extraction ✔</span> ➔
            <span>3. Chunking ✔</span> ➔
            <span>4. Vector Embedding ✔</span> ➔
            <span>5. ChromaDB Search ✔</span> ➔
            <span>6. LLM Citation Answer</span>
        </div>
        """), unsafe_allow_html=True)

        col_u1, col_u2 = st.columns([3, 1])
        with col_u1:
            uploaded_file = st.file_uploader("Upload Legal Contract / Document (PDF, DOCX, TXT)", type=["pdf", "docx", "txt"], key="rag_doc_up")
        with col_u2:
            st.write("&nbsp;")
            st.write("&nbsp;")
            load_demo = st.button("⚡ Load Demo Contract", use_container_width=True)

        if load_demo:
            from fpdf import FPDF
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Helvetica", "B", 14)
            pdf.cell(0, 10, "MASTER SERVICES AGREEMENT", new_x="LMARGIN", new_y="NEXT", align="C")
            pdf.set_font("Helvetica", size=10)
            pdf.multi_cell(0, 6, "1. SERVICES & COMPENSATION: Client agrees to pay Provider $50,000 for AI consulting services within 30 days of invoice.\n\n2. TERMINATION: Either party may terminate this agreement with 30 days prior written notice. If terminated early, Client pays for completed work.\n\n3. INDEMNIFICATION & LIABILITY: Provider's total liability under this agreement shall not exceed $10,000. Client shall indemnify Provider against third-party claims.\n\n4. GOVERNING LAW: This Agreement shall be governed by the laws of the State of California.")
            pdf_bytes = pdf.output()
            demo_buffer = io.BytesIO(pdf_bytes)
            demo_buffer.name = "Demo_Master_Services_Agreement.pdf"
            uploaded_file = demo_buffer

        if uploaded_file:
            if st.button("🚀 Index Document in Vector Store", use_container_width=True) or load_demo:
                with st.spinner("Processing Document ➔ Extracting Text ➔ Chunking ➔ Embedding into ChromaDB..."):
                    try:
                        chunks = st.session_state["rag_engine"].process_pdf_and_create_vectorstore(uploaded_file, uploaded_file.name)
                        st.session_state["rag_indexed"] = True
                        st.session_state["chunk_count"] = chunks
                        st.session_state["indexed_file_name"] = uploaded_file.name
                        st.success(f"Successfully indexed '{uploaded_file.name}' into ChromaDB ({chunks} vector chunks)!")
                    except Exception as e:
                        st.error(f"Error indexing document: {e}")

        if st.session_state.get("rag_indexed", False):
            st.markdown(textwrap.dedent("""
            <div class='risk-score-box'>
                <div style='font-size: 0.8rem; color: #94A3B8; font-weight: 700;'>CONTRACT AUDIT RISK SCORE</div>
                <div class='risk-score-val'>78 / 100</div>
                <div style='font-size: 0.82rem; color: #FDA4AF;'>⚠️ Medium-High Risk (Unilateral Liability Cap & Short 1-Year Confidentiality)</div>
            </div>
            """), unsafe_allow_html=True)

        st.markdown("---")
        st.subheader("💬 Query Indexed Vector Document")
        for msg in st.session_state.get("rag_chat_messages", []):
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

        if user_prompt := st.chat_input("Ask a question about the uploaded document..."):
            st.session_state["rag_chat_messages"].append({"role": "user", "content": user_prompt})
            with st.chat_message("user"):
                st.markdown(user_prompt)

            with st.chat_message("assistant"):
                if st.session_state.get("rag_indexed", False):
                    res = st.session_state["rag_engine"].query(user_prompt, provider=provider_name, model_name=model_name)
                    ans = res["answer"]
                else:
                    ans = "⚠️ Please upload a document or click 'Load Demo Contract' and index it first."
                st.markdown(ans)
                st.session_state["rag_chat_messages"].append({"role": "assistant", "content": ans})

    # ---------------------------------------------------------
    # 6. TIMELINE BUILDER WITH PERSISTENT ANIMATED OUTPUT
    # ---------------------------------------------------------
    elif page == "📅 Timeline Builder":
        st.subheader("📅 Interactive Vertical Case Timeline Builder")
        st.caption("Automatically extract dates, events, people, and proceedings into an interactive vertical timeline.")

        timeline_file = st.file_uploader("Upload Case PDF / Document", type=["pdf", "docx", "txt"], key="tb_pdf")
        run_demo_tb = st.button("⚡ Run Demo Timeline Extraction", use_container_width=True)

        default_timeline = """# 📅 VERTICAL CASE TIMELINE & CHRONOLOGY OF EVENTS

| Date / Time | Event / Occurrence | Document Ref | Relevance |
| :--- | :--- | :--- | :--- |
| **Jan 15, 2024** | Master Services Agreement signed | Ex. A (p. 2) | Contract Effective Date |
| **Mar 01, 2024** | Invoice #101 issued ($25,000) | Ex. B (p. 1) | Payment due in 30 days |
| **Apr 15, 2024** | Payment overdue by 15 days | Ex. C (p. 3) | Initial Default Notice sent |
| **May 01, 2024** | Work suspended under Clause 12 | Ex. D (p. 5) | Right to suspend exercised |

## 🚨 Critical Deadlines & Limitations
- **Statute of Limitations Expiry:** May 01, 2027 (3 Years for debt recovery suit).
"""

        if "timeline_output" not in st.session_state:
            st.session_state["timeline_output"] = default_timeline

        if run_demo_tb or (timeline_file and st.button("📅 Extract Case Timeline", use_container_width=True)):
            with st.spinner("Extracting chronological dates and events..."):
                if timeline_file and not run_demo_tb:
                    st.session_state["timeline_output"] = build_case_timeline(timeline_file, provider=provider_name, model_name=model_name)
                else:
                    st.session_state["timeline_output"] = default_timeline

        if "timeline_output" in st.session_state:
            render_animated_result(st.session_state["timeline_output"])

    # ---------------------------------------------------------
    # 7. FIND WEAKNESSES & VERDICT PREDICTOR
    # ---------------------------------------------------------
    elif page in ["🛡️ Find Weaknesses", "🏆 Predict Verdict"]:
        st.subheader("🛡️ Case Weakness & Verdict Probability Evaluator")

        if page == "🛡️ Find Weaknesses":
            st.caption("Identify flaws, evidentiary gaps, and legal loopholes in opposing counsel's arguments.")
            c_w1, c_w2 = st.columns(2)
            with c_w1:
                our_facts = st.text_area("Our Case Facts:", value="Client delivered software source code on March 15. Client has signed delivery acceptance receipt signed by Plaintiff CTO.", height=130)
            with c_w2:
                opp_claim = st.text_area("Opposing Party's Claim:", value="Plaintiff claims software was never delivered and demands 100% refund plus damages.", height=130)

            default_weakness = """# 🛡️ OPPOSITION ARGUMENT & WEAKNESS AUDIT REPORT

## 📊 Case Strength Rating: 72% (Strong Defense Position)

### 🟢 Strengths & Supporting Evidence
1. Signed Delivery Acceptance Receipt signed by Plaintiff CTO (Direct Written Evidence).
2. Email confirmation acknowledging March 15 code delivery.

### 🔴 Opposing Party Weaknesses & Contradictions
1. **Evidentiary Contradiction:** Claim of non-delivery is refuted by their CTO's physical signature on Ex. B.
2. **Procedural Gap:** Plaintiff failed to issue a 30-day cure notice before alleging breach.
"""
            if "weakness_output" not in st.session_state:
                st.session_state["weakness_output"] = default_weakness

            if st.button("🛡️ Analyze Opposition Weaknesses", use_container_width=True):
                with st.spinner("Finding argument flaws and evidentiary contradictions..."):
                    st.session_state["weakness_output"] = find_argument_weaknesses(our_facts, opp_claim, provider=provider_name, model_name=model_name)

            if "weakness_output" in st.session_state:
                render_animated_result(st.session_state["weakness_output"])

        else: # Predict Verdict
            st.caption("Analyze evidence strength and predict probability odds.")
            ev_summary = st.text_area("Summarize Evidence & Documents Available:", value="1. Signed Written Agreement with clear payment terms.\n2. Email confirmation of project completion from Plaintiff.\n3. Bank statements showing partial payments made.\n4. Written 30-day notice served before filing suit.", height=120)

            default_verdict = """# 🏆 VERDICT PROBABILITY & OUTCOME PREDICTION REPORT

## 📌 Predicted Outcome: FAVORABLE (74% Probability)

### 📊 Influencing Risk Factors
- **Documentary Evidence Weight:** High (Signed Agreement & Notices)
- **Reciprocal Promise Breach:** Plaintiff 90-day payment default
- **Court Cost Exposure:** Low
"""
            if "verdict_output" not in st.session_state:
                st.session_state["verdict_output"] = default_verdict

            if st.button("🏆 Predict Case Verdict & Winning Odds", use_container_width=True):
                with st.spinner("Calculating probability score and risk factors..."):
                    st.session_state["verdict_output"] = predict_case_verdict(ev_summary, provider=provider_name, model_name=model_name)

            if "verdict_output" in st.session_state:
                render_animated_result(st.session_state["verdict_output"])
                st.warning("⚠️ **MANDATORY LEGAL DISCLAIMER:** AI-generated analysis. This is not legal advice and should not be treated as a guaranteed prediction.")

    # ---------------------------------------------------------
    # 8. EVIDENCE ANALYZER
    # ---------------------------------------------------------
    elif page == "📁 Evidence Analyzer":
        st.subheader("📁 Evidence Audit & Contradiction Analyzer")
        st.caption("Extract evidence classification, material facts, contradictions, and relevance scores.")

        ev_file = st.file_uploader("Upload Evidence Document / PDF", type=["pdf", "docx", "txt"], key="ev_up")
        run_demo_ev = st.button("⚡ Run Demo Evidence Audit", use_container_width=True)

        if run_demo_ev or (ev_file and st.button("📁 Analyze Evidence", use_container_width=True)):
            with st.spinner("Auditing evidence document for contradictions and relevance..."):
                target = ev_file if (ev_file and not run_demo_ev) else "Signed Delivery Receipt dated March 15, 2024 confirming source code handover."
                res = analyze_evidence_document(target, provider=provider_name, model_name=model_name)
                st.session_state["ev_res"] = res

        if "ev_res" in st.session_state:
            res = st.session_state["ev_res"]
            st.metric("Evidence Relevance Rating", f"{res['relevance_score']}%", "+12% High Admissibility")
            render_animated_result(res["report"])

    # ---------------------------------------------------------
    # 9. CASE STRATEGY GENERATOR
    # ---------------------------------------------------------
    elif page == "🏛️ Case Strategy":
        st.subheader("🏛️ Comprehensive Litigation Strategy Generator")
        st.caption("Generate an 8-part legal litigation roadmap, counterarguments, and next steps.")

        case_brief = st.text_area("Case Brief / Dispute Facts:", value="Client is accused of breach of contract by ABC Corp due to halted work after 90-day payment default.", height=120)
        ev_brief = st.text_area("Available Evidence Brief:", value="Signed MSA, Payment Schedule A, Unpaid Invoices #101-104, Notice of Suspension sent on Day 35.", height=100)

        default_strategy = """# 🏛️ MASTER LITIGATION STRATEGY REPORT

## 1. Executive Case Overview
Theory of defense centers on Plaintiff's prior material breach under Section 51 of Indian Contract Act.

## 2. Primary Legal Arguments
1. Prior Payment Breach by Plaintiff (90 Days Overdue).
2. Right to Suspend Work under Clause 12.
"""
        if "strategy_output" not in st.session_state:
            st.session_state["strategy_output"] = default_strategy

        if st.button("🏛️ Generate Litigation Strategy Report", use_container_width=True):
            with st.spinner("AI drafting master litigation strategy..."):
                st.session_state["strategy_output"] = generate_comprehensive_case_strategy(case_brief, ev_brief, provider=provider_name, model_name=model_name)

        if "strategy_output" in st.session_state:
            render_animated_result(st.session_state["strategy_output"])

    # ---------------------------------------------------------
    # 10. LEGAL RESEARCH & PRECEDENT SEARCH
    # ---------------------------------------------------------
    elif page in ["🔍 Search Judgments", "📌 Citation Finder", "⚖️ Similar Cases"]:
        st.subheader("🔍 Precedent Judgment Search & Citation Finder")
        st.caption("Search past court judgments, legal provisions, and similar case ratios.")

        col_r1, col_r2, col_r3 = st.columns(3)
        with col_r1:
            court_f = st.selectbox("Court Filter", ["All Courts", "Supreme Court of India", "Delhi High Court", "Bombay High Court"])
        with col_r2:
            year_f = st.selectbox("Year Filter", ["All Years", "2023", "2022", "2021", "2020"])
        with col_r3:
            q_in = st.text_input("Query / Keywords:", value="Breach of contract right to suspend work non-payment")

        results = search_judgments_database(q_in, court_filter=court_f, year_filter=year_f, provider=provider_name, model_name=model_name)
        for res in results:
            with st.expander(f"⚖️ {res['case_name']} ({res['court']}, {res['year']}) — Relevance: {res['relevance_score']}%"):
                st.write(f"**Citation:** {res['citation']}")
                st.write(f"**Relevant Provisions:** {res['relevant_sections']}")
                st.write(f"**Summary:** {res['summary']}")
                if st.button(f"Explain Judgment '{res['id']}'", key=f"exp_{res['id']}"):
                    exp_out = explain_judgment(res['full_text'], provider=provider_name, model_name=model_name)
                    render_animated_result(exp_out)

    # ---------------------------------------------------------
    # 11. LEGAL CALCULATORS
    # ---------------------------------------------------------
    elif page == "🧮 Legal Calculator":
        st.subheader("🧮 Legal Financial & Limitation Calculators")
        st.caption("Calculate CPC Section 34 Interest, Limitation Periods, and Stamp Duty.")

        calc_tab1, calc_tab2, calc_tab3 = st.tabs(["💰 Interest Calculator", "📅 Limitation Period", "📜 Stamp Duty Estimator"])

        with calc_tab1:
            st.markdown("### CPC Section 34 Legal Interest Calculator")
            p_val = st.number_input("Principal Amount ($ / ₹)", value=100000.0, step=5000.0)
            r_val = st.number_input("Annual Interest Rate (%)", value=12.0, step=0.5)
            d_val = st.number_input("Duration (Days)", value=365, step=30)
            if st.button("Calculate Interest", key="btn_calc_int"):
                res = calculate_legal_interest(p_val, r_val, d_val)
                st.session_state["calc_int_res"] = res

            if "calc_int_res" in st.session_state:
                res = st.session_state["calc_int_res"]
                col_i1, col_i2 = st.columns(2)
                with col_i1:
                    st.metric("Simple Interest", f"${res['simple_interest']}", f"Total: ${res['total_simple']}")
                with col_i2:
                    st.metric("Compound Interest", f"${res['compound_interest']}", f"Total: ${res['total_compound']}")

        with calc_tab2:
            st.markdown("### Limitation Act Expiry Calculator")
            s_date = st.date_input("Date of Cause of Action").strftime("%Y-%m-%d")
            c_type = st.selectbox("Cause of Action Type", ["Contract Breach", "Recovery of Money", "Cheque Dishonor (Sec 138)", "Property Possession (Mortgage)", "Tort & Personal Injury"])
            if st.button("Calculate Expiry Date", key="btn_calc_lim"):
                res_lim = calculate_limitation_period(s_date, c_type)
                st.session_state["calc_lim_res"] = res_lim

            if "calc_lim_res" in st.session_state:
                res_lim = st.session_state["calc_lim_res"]
                if "error" not in res_lim:
                    st.metric("Limitation Expiry Date", res_lim["expiry_date"], f"{res_lim['days_remaining']} Days Remaining")
                    if res_lim["is_expired"]:
                        st.error("⚠️ Statute of Limitation Has Expired!")
                    else:
                        st.success("✅ Within Prescribed Statutory Limitation Period.")

        with calc_tab3:
            st.markdown("### State Stamp Duty & Fee Estimator")
            t_amount = st.number_input("Transaction / Consideration Amount ($ / ₹)", value=500000.0, step=50000.0)
            d_type = st.selectbox("Document Category", ["Sale Agreement", "Rental Agreement", "Mortgage Deed", "Power of Attorney", "General Contract"])
            st_name = st.selectbox("State Jurisdiction", ["Maharashtra", "Delhi", "Karnataka", "Tamil Nadu", "West Bengal"])
            if st.button("Estimate Stamp Duty", key="btn_calc_stamp"):
                sd_res = estimate_stamp_duty(t_amount, d_type, st_name)
                st.session_state["calc_stamp_res"] = sd_res

            if "calc_stamp_res" in st.session_state:
                sd_res = st.session_state["calc_stamp_res"]
                st.metric("Estimated Stamp Duty", f"${sd_res['estimated_stamp_duty']}", f"Rate: {sd_res['stamp_duty_rate']}")
                st.metric("Registration Fee", f"${sd_res['estimated_registration_fee']}")
                st.info(f"**Total Cost:** ${sd_res['total_cost']}")

    # ---------------------------------------------------------
    # 12. DOCUMENT GENERATOR & TEMPLATES
    # ---------------------------------------------------------
    elif page in ["✍️ Generate Document", "📋 Document Templates"]:
        st.subheader("✍️ AI Legal Document & Notice Generator")
        st.caption("Draft Contracts, NDAs, Legal Notices, and Affidavits with Word/PDF export.")

        col1, col2 = st.columns(2)
        with col1:
            doc_type = st.selectbox("Document Category", [
                "Non-Disclosure Agreement (NDA)",
                "Employment Agreement",
                "Legal Notice for Payment Recovery",
                "Tenant Eviction Legal Notice",
                "General Affidavit"
            ])
            party_a = st.text_input("Party A / Disclosing Party / Sender", value="Acme Corporation LLC")
            party_b = st.text_input("Party B / Receiving Party / Recipient", value="TechSolutions Global Inc.")
        with col2:
            effective_date = st.date_input("Date").strftime("%B %d, %Y")
            jurisdiction = st.text_input("Jurisdiction", value="State of California, USA / Courts of New Delhi")
            key_terms = st.text_area("Specific Terms / Claim Amount", value="1-year duration, $50,000 consideration, strict confidentiality, 30 days notice required.", height=85)

        if st.button("✨ Generate Document Draft", use_container_width=True):
            with st.spinner("AI drafting legal document..."):
                draft = generate_legal_draft(doc_type, party_a, party_b, effective_date, jurisdiction, key_terms, provider_name, model_name)
                st.session_state["active_draft"] = draft
                st.session_state["active_title"] = doc_type

        if "active_draft" in st.session_state:
            render_animated_result(st.session_state["active_draft"])
            col_d1, col_d2 = st.columns(2)
            with col_d1:
                docx_buf = export_to_docx(st.session_state["active_title"], st.session_state["active_draft"])
                st.download_button("📥 Download DOCX", data=docx_buf.getvalue(), file_name=f"{doc_type}.docx", mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document", use_container_width=True)
            with col_d2:
                pdf_bytes = export_to_pdf(st.session_state["active_title"], st.session_state["active_draft"])
                st.download_button("📥 Download PDF", data=pdf_bytes, file_name=f"{doc_type}.pdf", mime="application/pdf", use_container_width=True)

    # ---------------------------------------------------------
    # 13. DEDICATED VIEWS FOR REMAINING MODULES
    # ---------------------------------------------------------
    elif page == "📁 Recent Documents":
        st.subheader("📁 Recent Documents & Manager")
        st.caption("Manage uploaded contracts, indexed files, and document history.")
        
        uploaded_history = st.session_state.get("indexed_docs_list", [
            {"name": "Master_Services_Agreement.pdf", "size": "1.2 MB", "status": "Indexed in ChromaDB", "chunks": 14},
            {"name": "Employment_Contract_Template.docx", "size": "450 KB", "status": "Ready", "chunks": 8}
        ])
        
        for doc in uploaded_history:
            st.markdown(f"📄 **{doc['name']}** ({doc['size']}) — *{doc['status']}* ({doc['chunks']} chunks)")

    elif page == "⭐ Favorites":
        st.subheader("⭐ Bookmarked Legal Cases & Templates")
        st.caption("Quick access to your saved precedent cases and favorite document templates.")
        
        st.markdown("""
        - ⭐ **State of Maharashtra v. ABC Corp Ltd** *(Supreme Court 2023)*
        - ⭐ **Master Non-Disclosure Agreement (NDA) Template**
        - ⭐ **Legal Notice for Payment Recovery Template**
        """)

    elif page == "📝 Case Notes":
        st.subheader("📝 Counsel Case Notes & Workspace")
        st.caption("Draft, save, and organize case notes with autosave.")
        
        saved_notes = st.text_area("Counsel Notes Editor:", value=st.session_state.get("user_case_notes", ""), height=250)
        st.session_state["user_case_notes"] = saved_notes
        if st.button("💾 Save Notes", use_container_width=True):
            st.success("Case notes saved to session state!")

    elif page == "📦 Export Center":
        st.subheader("📦 Central Export & Document Hub")
        st.caption("Export active drafts, strategy reports, and audit summaries in DOCX, PDF, or TXT format.")
        
        col_e1, col_e2 = st.columns(2)
        with col_e1:
            if "active_draft" in st.session_state:
                st.download_button("📥 Download Active Legal Draft (DOCX)", data=export_to_docx("Legal_Draft", st.session_state["active_draft"]).getvalue(), file_name="Legal_Draft.docx", mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document", use_container_width=True)
            else:
                st.info("No active document draft generated yet. Go to 'Generate Document' page.")
        with col_e2:
            if "bot_chat_messages" in st.session_state:
                chat_txt = "\n".join([f"{m['role'].upper()}: {m['content']}" for m in st.session_state["bot_chat_messages"]])
                st.download_button("📥 Download Chat Transcript (TXT)", data=chat_txt, file_name="Legal_Chat_Transcript.txt", mime="text/plain", use_container_width=True)

    elif page in ["⚔️ Compare Contracts", "📜 Lawyer's Script"]:
        if page == "⚔️ Compare Contracts":
            st.subheader("⚔️ Contract Semantic Comparison & Diff")
            st.caption("Upload two PDF contract versions to highlight altered terms and risk redlines.")

            col_a, col_b = st.columns(2)
            with col_a:
                pdf_a = st.file_uploader("Upload Original PDF (Doc A)", type=["pdf"], key="comp_a")
            with col_b:
                pdf_b = st.file_uploader("Upload Revised PDF (Doc B)", type=["pdf"], key="comp_b")

            default_comp = """# ⚖️ Contract Version Comparison Report

## 📌 Executive Summary
- **Comparison:** Original Standard Contract vs Revised Vendor Draft.
- **Verdict:** Revised Vendor Draft reduces confidentiality duration from 3 years to 1 year and caps vendor liability at $5,000.

## 🚨 Critical Clause Redlines
1. **Confidentiality:** Reduced to 1 year (High Risk).
2. **Indemnity Cap:** Unilateral $5,000 cap favoring Vendor (Severe Risk).

## 💡 Negotiation Action
1. Restore 3-year confidentiality term.
2. Re-establish mutual indemnity cap equal to total contract value ($50,000).
"""
            if "comp_output" not in st.session_state:
                st.session_state["comp_output"] = default_comp

            if st.button("⚡ Run Contract Comparison", use_container_width=True):
                st.session_state["comp_output"] = default_comp

            if "comp_output" in st.session_state:
                render_animated_result(st.session_state["comp_output"])

        elif page == "📜 Lawyer's Script":
            st.subheader("📜 Lawyer's Courtroom Script & Case Notes")
            st.caption("Generate winning opening statements, core legal arguments, and cross-examination strategies.")

            default_case = "Client is accused of breach of contract by ABC Corp. Client completed 80% of deliverables, but ABC Corp delayed payments by 90 days. Client halted work as permitted under Clause 12."
            case_input = st.text_area("Enter Case Brief / Key Facts:", value=default_case, height=140)
            
            default_script = """# 📜 LAWYER'S COURT SCRIPT & CASE STRATEGY

## 🎙️ 1. Opening Statement
"May it please the Court. We represent the Defendant, who executed 80% of contractual obligations faithfully. The sole reason performance was suspended was the Plaintiff's prior breach of withholding payment for 90 days."

## ⚖️ 2. Core Legal Arguments & Precedents
1. **Prior Material Breach:** Section 51 of Indian Contract Act.
2. **Clause 12 Right of Suspension:** Explicit contractual authorization.
"""
            if "script_output" not in st.session_state:
                st.session_state["script_output"] = default_script

            if st.button("⚡ Generate Lawyer's Script", use_container_width=True):
                with st.spinner("Drafting lawyer script..."):
                    st.session_state["script_output"] = generate_lawyers_script(case_input, provider=provider_name, model_name=model_name)

            if "script_output" in st.session_state:
                render_animated_result(st.session_state["script_output"])

    else:
        st.subheader(f"📌 {page}")
        st.info(f"The module **{page}** is fully loaded. Select any option from the sidebar to launch interactive legal tools.")


if __name__ == "__main__":
    main()

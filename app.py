import streamlit as st
import os
from dotenv import load_dotenv
from utils import extract_text_from_pdf
from analysis_engine import CareerAI

# 1. Page Configuration (Must be first)
st.set_page_config(
    page_title="CareerForge AI",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load environment variables
load_dotenv()

# --- ENHANCED PROFESSIONAL CSS ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    /* Root Variables for Consistent Theming */
    :root {
        --primary-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        --secondary-gradient: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        --success-gradient: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        --card-bg: rgba(30, 35, 43, 0.95);
        --glass-bg: rgba(255, 255, 255, 0.05);
        --border-color: rgba(255, 255, 255, 0.1);
        --text-primary: #ffffff;
        --text-secondary: #b0b3b8;
        --shadow-lg: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
        --shadow-sm: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
    }

    /* Main App Styling */
    .stApp {
        background: linear-gradient(135deg, #0c0e1a 0%, #1a1f2e 50%, #16213e 100%);
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        backdrop-filter: blur(10px);
    }

    /* Glassmorphism Cards */
    .glass-card {
        background: var(--glass-bg);
        backdrop-filter: blur(20px);
        border: 1px solid var(--border-color);
        border-radius: 20px;
        padding: 2rem;
        box-shadow: var(--shadow-lg);
        position: relative;
        overflow: hidden;
    }
    .glass-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 1px;
        background: var(--primary-gradient);
    }

    /* Enhanced Metric Cards */
    .metric-card {
        background: var(--card-bg);
        border: 1px solid var(--border-color);
        border-radius: 16px;
        padding: 1.5rem;
        text-align: center;
        box-shadow: var(--shadow-sm);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: var(--shadow-lg);
    }
    .metric-value {
        font-size: 2.5rem;
        font-weight: 800;
        color: #ffffff;        /* <-- always visible digits */
        margin-bottom: 0.5rem;
    }
    .metric-label {
        color: var(--text-secondary);
        font-weight: 500;
        font-size: 0.95rem;
        letter-spacing: 0.5px;
    }

    /* Professional Button Styling */
    .stButton > button {
        background: var(--primary-gradient);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 14px 32px;
        font-weight: 600;
        font-size: 1rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: var(--shadow-sm);
        width: 100%;
        position: relative;
        overflow: hidden;
    }
    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 20px 40px rgba(102, 126, 234, 0.4);
    }
    .stButton > button:active {
        transform: translateY(-1px);
    }

    /* Input Fields */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        background: rgba(30, 35, 43, 0.8);
        color: var(--text-primary);
        border: 1px solid var(--border-color);
        border-radius: 12px;
        padding: 12px 16px;
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
    }
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        transform: translateY(-1px);
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, rgba(12, 14, 26, 0.95) 0%, rgba(26, 31, 46, 0.95) 100%);
        border-right: 1px solid var(--border-color);
        backdrop-filter: blur(20px);
    }

    /* Hero Text */
    .hero-title {
        background: var(--success-gradient);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-weight: 800;
        font-size: 3.5rem;
        line-height: 1.1;
        text-align: center;
        margin-bottom: 1rem;
        letter-spacing: -2px;
    }
    .hero-subtitle {
        color: var(--text-secondary);
        font-size: 1.3rem;
        text-align: center;
        font-weight: 400;
        max-width: 600px;
        margin: 0 auto;
    }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.5rem;
    }
    .stTabs [data-baseweb="tab"] {
        background: var(--glass-bg);
        border: 1px solid var(--border-color);
        border-radius: 12px;
        padding: 12px 24px;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(102, 126, 234, 0.1);
        border-color: #667eea;
    }

    /* Success Messages */
    .stSuccess > div > div {
        background: rgba(79, 172, 254, 0.15);
        border: 1px solid rgba(79, 172, 254, 0.3);
        border-radius: 12px;
        padding: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# --- SESSION STATE ---
if "resume_text" not in st.session_state:
    st.session_state.resume_text = None
if "job_desc" not in st.session_state:
    st.session_state.job_desc = None
if "analysis_result" not in st.session_state:
    st.session_state.analysis_result = None
if "match_score" not in st.session_state:
    st.session_state.match_score = 0

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("### 🛠️ AI Configuration")

    env_api_key = os.getenv("GROQ_API_KEY")
    if not env_api_key:
        st.text_input("🔑 Groq API Key", type="password", key="api_key_input")
        if st.session_state.get("api_key_input"):
            os.environ["GROQ_API_KEY"] = st.session_state.api_key_input
            st.rerun()

    st.divider()
    st.markdown("### 🧠 Model Selection")
    selected_model = st.selectbox(
        "Choose AI Model",
        ["llama-3.3-70b-versatile", "llama-3.1-8b-instant", "mixtral-8x7b-32768"],
        index=0
    )
    temperature = st.slider("Creativity Level", 0.0, 1.0, 0.2, 0.1)

    st.divider()
    st.markdown("*Powered by Groq*")

# --- HERO ---
st.markdown('<div class="hero-title">CareerForge AI</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="hero-subtitle">Optimize your resume for the ATS era with semantic AI & LLM-powered insights.</div>',
    unsafe_allow_html=True
)

# --- INPUT SECTION ---
st.markdown("---")
with st.container():
    col1, col2 = st.columns([1, 1], gap="large")

    with col1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("📄 Upload Resume")
        uploaded_file = st.file_uploader(
            "Drop your PDF resume",
            type=["pdf"],
            label_visibility="collapsed",
            key="file_upload"
        )
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("💼 Job Description")
        job_desc_input = st.text_area(
            "Paste job description",
            height=180,
            label_visibility="collapsed",
            placeholder="Paste the full job description here..."
        )
        st.markdown('</div>', unsafe_allow_html=True)

# --- ACTION BUTTON ---
st.markdown("---")
c1, c2, c3 = st.columns([1, 2, 1])
with c2:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    analyze_btn = st.button("🚀 ANALYZE & OPTIMIZE", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# --- LOGIC ---
if analyze_btn:
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        st.error("⚠️ Please enter your Groq API key in the sidebar.")
    elif not uploaded_file or not job_desc_input.strip():
        st.warning("⚠️ Please upload a resume PDF and paste a job description.")
    else:
        with st.spinner("🔬 Analyzing semantic alignment & generating insights..."):
            try:
                agent = CareerAI(model_name=selected_model, temperature=temperature)
                text = extract_text_from_pdf(uploaded_file)
                agent.create_knowledge_base(text)
                score = agent.calculate_similarity(job_desc_input)
                analysis = agent.analyze_profile(text, job_desc_input)

                st.session_state.resume_text = text
                st.session_state.job_desc = job_desc_input
                st.session_state.match_score = score
                st.session_state.analysis_result = analysis

                st.success("✅ Analysis complete! Scroll down for insights.")
            except Exception as e:
                st.error(f"❌ Analysis failed: {str(e)}")

# --- RESULTS DASHBOARD ---
if st.session_state.analysis_result:
    st.markdown("---")

    m1, m2, m3, m4 = st.columns(4, gap="large")

    def metric_card(label, value, color="#4CAF50"):
        return f"""
        <div class="metric-card">
            <div class="metric-value" style="color: {color};">{value}</div>
            <div class="metric-label">{label}</div>
        </div>
        """

    score = st.session_state.match_score
    score_color = "#4facfe" if score > 70 else "#f093fb" if score > 50 else "#ff6b6b"

    with m1:
        st.markdown(metric_card("Match Score", f"{score:.0f}%", score_color), unsafe_allow_html=True)
    with m2:
        st.markdown(
            metric_card("Words", f"{len(st.session_state.resume_text.split()):,}", "#667eea"),
            unsafe_allow_html=True
        )
    with m3:
        read_time = len(st.session_state.resume_text.split()) // 200 + 1
        st.markdown(
            metric_card("Read Time", f"{read_time} min", "#f39c12"),
            unsafe_allow_html=True
        )
    with m4:
        st.markdown(
            metric_card("AI Model", selected_model.split("-")[0].upper(), "#00d4aa"),
            unsafe_allow_html=True
        )

    tab1, tab2, tab3 = st.tabs(["📊 AI Analysis Report", "✨ Smart Rewrite", "📝 Cover Letter"])

    with tab1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("### 🔍 Executive Summary")
        st.markdown(st.session_state.analysis_result)
        st.markdown('</div>', unsafe_allow_html=True)

    with tab2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        if st.button("✨ Generate ATS‑Optimized Summary", use_container_width=True):
            with st.spinner("Optimizing your profile..."):
                agent = CareerAI(model_name=selected_model, temperature=temperature)
                prompt = f"""Rewrite this resume summary to strongly match this job description.
Use ATS keywords naturally and strong action verbs.

JD: {st.session_state.job_desc[:400]}...
Resume: {st.session_state.resume_text[:600]}"""
                result = agent.llm.invoke(prompt).content
                st.success(result)
        st.markdown('</div>', unsafe_allow_html=True)

    with tab3:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        if st.button("✉️ Generate Cover Letter", use_container_width=True):
            with st.spinner("Crafting personalized letter..."):
                agent = CareerAI(model_name=selected_model, temperature=0.3)
                cover_letter = agent.generate_cover_letter(
                    st.session_state.resume_text,
                    st.session_state.job_desc
                )
                st.markdown("### 📄 Your Cover Letter")
                st.markdown(cover_letter)
                st.download_button(
                    "💾 Download Cover Letter",
                    cover_letter,
                    "cover_letter.md",
                    "text/markdown"
                )
        st.markdown('</div>', unsafe_allow_html=True)

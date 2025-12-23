import warnings
# Filter out annoying FAISS and library deprecation warnings to keep UI clean
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=RuntimeWarning)
warnings.filterwarnings("ignore", module="duckduckgo_search")
import streamlit as st
import os
import json
import re
from dotenv import load_dotenv
from streamlit_agraph import agraph
from annotated_text import annotated_text
from src.ui_styles import apply_custom_css, display_metric_card
from src.pdf_handler import extract_text_from_pdf
from src.llm_engine import CareerAI
from src.graph_builder import build_skill_graph
from src.pdf_gen import create_pdf_report
from src.web_search import get_company_info

# 1. Config & Setup
st.set_page_config(page_title="CareerForge AI", page_icon="🚀", layout="wide")
load_dotenv()
apply_custom_css()

# 2. Session State Initialization
if "resume_text" not in st.session_state: st.session_state.resume_text = None
if "job_desc" not in st.session_state: st.session_state.job_desc = None
if "analysis_result" not in st.session_state: st.session_state.analysis_result = None
if "graph_data" not in st.session_state: st.session_state.graph_data = None
if "interview_q" not in st.session_state: st.session_state.interview_q = None
if "matched_keywords" not in st.session_state: st.session_state.matched_keywords = []
if "history" not in st.session_state: st.session_state.history = []
if "company_context" not in st.session_state: st.session_state.company_context = ""
if "match_score" not in st.session_state: st.session_state.match_score = 0

# 3. Sidebar Configuration
with st.sidebar:
    # --- LOGO SECTION ---
    logo_col1, logo_col2 = st.columns([1, 4])
    with logo_col1:
        st.image("https://cdn-icons-png.flaticon.com/512/12308/12308783.png", width=50)
    with logo_col2:
        st.markdown("<h2 style='margin-top: 5px; margin-bottom: 0; font-size: 1.5rem;'>CareerForge</h2>", unsafe_allow_html=True)
        st.caption("AI-Powered Architect")
    
    st.markdown("---")
    
    # --- CONTROL PANEL ---
    st.markdown("### ⚙️ Control Panel")
    
    # API Key
    if not os.getenv("GROQ_API_KEY"):
        os.environ["GROQ_API_KEY"] = st.text_input("🔑 Groq API Key", type="password", help="Get free key at console.groq.com")
    
    # AI Config
    model = st.selectbox("🧠 AI Model", ["llama-3.3-70b-versatile", "llama-3.1-8b-instant"])
    persona = st.selectbox("🎭 Reviewer Persona", ["HR Recruiter", "Senior Engineer", "CTO"])
    temp = st.slider("🌡️ Creativity Level", 0.0, 1.0, 0.1)
    
    st.markdown("---")
    
    # --- COMPANY INTELLIGENCE ---
    st.markdown("### 🏢 Target Intelligence")
    company_name = st.text_input("Target Company", placeholder="e.g. Netflix, OpenAI")
    
    # --- HISTORY TRACKER ---
    if st.session_state.history:
        st.markdown("---")
        st.markdown("### 🕒 Recent Scans")
        for item in st.session_state.history[-3:]: # Show last 3
             st.markdown(f"""
            <div style='background: rgba(255,255,255,0.05); padding: 8px; border-radius: 5px; margin-bottom: 5px; font-size: 0.85rem;'>
                <strong>{item['company']}</strong> <span style='float: right; color: #4CAF50;'>{item['score']}%</span>
            </div>
            """, unsafe_allow_html=True)

    # PDF Download Button
    if st.session_state.analysis_result:
        st.markdown("---")
        st.markdown("### 📥 Export")
        missing = []
        if st.session_state.graph_data:
            missing = st.session_state.graph_data.get('missing_skills', [])
        
        pdf_file = create_pdf_report(
            name="Candidate", 
            score=st.session_state.match_score, 
            analysis=st.session_state.analysis_result,
            missing_skills=missing
        )
        
        st.download_button(
            label="📄 Download Full Report",
            data=pdf_file,
            file_name="CareerForge_Report.pdf",
            mime="application/pdf"
        )

# 4. Main UI Layout
# Hero Header
st.markdown("""
<div style="text-align: center; margin-bottom: 40px;">
    <h1 style="font-size: 3.5rem; margin-bottom: 10px;">CareerForge AI</h1>
    <p style="font-size: 1.2rem; color: #B0B3B8;">Optimize your profile, master the interview, and land the job.</p>
</div>
""", unsafe_allow_html=True)

# Input Section (Styled Card)
with st.container():
    st.markdown("<div class='metric-card' style='text-align: left; padding: 30px;'>", unsafe_allow_html=True)
    col1, col2 = st.columns([1, 1], gap="large")
    with col1:
        st.markdown("#### 📄 Upload Resume")
        uploaded_file = st.file_uploader("Upload PDF", type=["pdf"], label_visibility="collapsed")
    with col2:
        st.markdown("#### 💼 Job Description")
        job_desc = st.text_area("Paste JD", height=150, label_visibility="collapsed", placeholder="Paste the job description here...")
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# 5. ANALYSIS LOGIC
# Centered Analyze Button
c1, c2, c3 = st.columns([1, 2, 1])
with c2:
    analyze_btn = st.button("🔍 Analyze & Optimize Profile", type="primary")

if analyze_btn:
    if uploaded_file and job_desc and os.getenv("GROQ_API_KEY"):
        with st.spinner("🚀 Analyzing Profile & Researching Company..."):
            try:
                # Init Agent
                agent = CareerAI(model, temp)
                text = extract_text_from_pdf(uploaded_file)
                
                # --- SMART COMPANY SEARCH ---
                company_context = ""
                if company_name:
                    # 1. Try Web Search
                    web_data = get_company_info(company_name)
                    
                    if web_data:
                        company_context = web_data
                    else:
                        # 2. Fallback to LLM Knowledge (If Rate Limited)
                        st.toast("Web search limit reached. Using AI Knowledge.", icon="🧠")
                        company_context = agent.generate_company_insight(company_name)
                        
                    st.session_state.company_context = company_context
                # ----------------------------
                
                # Run Core Analysis Pipeline
                agent.create_knowledge_base(text)
                score = agent.calculate_similarity(job_desc)
                analysis = agent.analyze_profile(text, job_desc, persona)
                
                # Update Session State
                st.session_state.resume_text = text
                st.session_state.job_desc = job_desc
                st.session_state.match_score = score
                st.session_state.analysis_result = analysis
                st.session_state.graph_data = None 
                st.session_state.matched_keywords = [] # Reset
                
                # Save to History
                st.session_state.history.append({
                    "company": company_name if company_name else "Unknown",
                    "score": score
                })
                
            except Exception as e:
                st.error(f"Analysis Failed: {str(e)}")
    else:
        st.warning("⚠️ Please provide Groq API Key, Resume, and Job Description.")

# 6. RESULTS DASHBOARD
if st.session_state.analysis_result:
    st.divider()
    
    # Metrics Row
    m1, m2, m3, m4 = st.columns(4)
    display_metric_card(m1, "Match Score", f"{st.session_state.match_score}%")
    display_metric_card(m2, "Word Count", len(st.session_state.resume_text.split()))
    display_metric_card(m3, "Persona", persona)
    intel_status = "Active" if st.session_state.company_context else "None"
    display_metric_card(m4, "Company Intel", intel_status)
    
    st.markdown("<br>", unsafe_allow_html=True)

    # Tabs
    tabs = st.tabs([
        "📊 Analysis", 
        "🔥 Heatmap", 
        "🕸️ Skill Graph", 
        "🎙️ Interview", 
        "📧 Cold Email", 
        "📝 Rewrite",
        "🎓 Up-Skill"
    ])
    
    # Re-init agent for tab interactions
    agent = CareerAI(model, temp)
    
    # --- TAB 1: Analysis Report ---
    with tabs[0]:
        st.markdown("### 📑 AI Consultant Report")
        st.markdown(st.session_state.analysis_result)
        if st.session_state.company_context:
            st.info("💡 **Company Context Used:**")
            st.markdown(st.session_state.company_context)
        
    # --- TAB 2: ATS Heatmap ---
    with tabs[1]:
        st.subheader("🔥 ATS Keyword Heatmap")
        st.info("Highlights technical keywords from the JD found in your resume.")
        
        if st.button("Generate Heatmap"):
            with st.spinner("Scanning..."):
                keywords = agent.extract_matched_keywords(st.session_state.resume_text, st.session_state.job_desc)
                st.session_state.matched_keywords = keywords
        
        if st.session_state.matched_keywords:
            body = st.session_state.resume_text
            # Regex to find keywords case-insensitively
            pattern = re.compile(f"({'|'.join([re.escape(k) for k in st.session_state.matched_keywords])})", re.IGNORECASE)
            parts = pattern.split(body)
            annotated_parts = []
            for part in parts:
                if part.lower() in [k.lower() for k in st.session_state.matched_keywords]:
                    annotated_parts.append((part, "MATCH", "#8ef"))
                else:
                    annotated_parts.append(part)
            annotated_text(*annotated_parts)

    # --- TAB 3: Skill Graph ---
    with tabs[2]:
        st.subheader("🕸️ Skill Gap Visualization")
        if st.button("Generate Graph"):
            with st.spinner("Mapping Skills..."):
                json_str = agent.extract_skills_json(st.session_state.resume_text, st.session_state.job_desc)
                try:
                    data = json.loads(json_str)
                    st.session_state.graph_data = data
                except: st.error("Failed to parse graph data.")
        
        if st.session_state.graph_data:
            nodes, edges, config = build_skill_graph(
                st.session_state.graph_data.get('present_skills', []), 
                st.session_state.graph_data.get('missing_skills', [])
            )
            agraph(nodes=nodes, edges=edges, config=config)

    # --- TAB 4: Mock Interview ---
    with tabs[3]:
        st.subheader("🎙️ AI Technical Interviewer")
        st.info("The AI will ask a tough question based on your missing skills.")
        
        if st.button("Generate Question"):
            with st.spinner("Thinking..."):
                skills = "general gaps"
                if st.session_state.graph_data:
                    skills = ", ".join(st.session_state.graph_data.get('missing_skills', []))
                st.session_state.interview_q = agent.generate_interview_question(st.session_state.job_desc, skills)
        
        if st.session_state.interview_q:
            st.markdown(f"**Q:** *{st.session_state.interview_q}*")
            audio = st.audio_input("Record Answer")
            if audio:
                with st.spinner("Transcribing & Grading..."):
                    # Use read() directly on the Streamlit audio object
                    text = agent.transcribe_audio(audio.read())
                    st.success(f"**You said:** {text}")
                    feedback = agent.evaluate_interview_answer(st.session_state.interview_q, text)
                    st.markdown("### 👨‍🏫 Feedback")
                    st.markdown(feedback)

    # --- TAB 5: Cold Email ---
    with tabs[4]:
        st.subheader("📧 Networking Outreach")
        recipient = st.selectbox("Recipient Role", ["Hiring Manager", "Technical Recruiter", "Alumni / Peer"])
        
        if st.button("Draft Cold Email"):
            with st.spinner("Drafting..."):
                email_draft = agent.generate_cold_email(
                    st.session_state.resume_text, 
                    st.session_state.job_desc, 
                    st.session_state.company_context, 
                    recipient
                )
                st.text_area("Copy this Draft:", email_draft, height=250)
                
    # --- TAB 6: Rewrite ---
    with tabs[5]:
        st.subheader("✍️ Summary Rewrite")
        if st.button("Rewrite Summary"):
            with st.spinner("Rewriting..."):
                prompt = f"Rewrite resume summary for {company_name} job: {st.session_state.job_desc[:300]}... Original: {st.session_state.resume_text[:500]}"
                res = agent.llm.invoke(prompt).content
                st.success(res)
    
    # --- TAB 7: Up-Skill (NEW) ---
    with tabs[6]:
        st.subheader("🚀 Accelerated Learning Plan")
        st.info("The fastest way to learn is to build. Here is a custom project idea to fill your gaps.")
        
        if st.button("Generate Learning Roadmap"):
            with st.spinner("Designing curriculum..."):
                skills = st.session_state.graph_data.get('missing_skills', []) if st.session_state.graph_data else "General Upskilling"
                if isinstance(skills, list): 
                    skills = ", ".join(skills)
                
                plan = agent.generate_learning_plan(skills)
                st.markdown(plan)
                
                st.divider()
                st.markdown("### 📚 Recommended Search Queries")
                for skill in skills.split(","):
                    if skill.strip():
                        st.markdown(f"- [Learn {skill.strip()} in 10 minutes](https://www.youtube.com/results?search_query=learn+{skill.strip()}+crash+course)")
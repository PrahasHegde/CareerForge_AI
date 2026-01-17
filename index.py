import warnings
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
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=RuntimeWarning)
warnings.filterwarnings("ignore", module="duckduckgo_search")

st.set_page_config(page_title="CareerForge AI", page_icon="🚀", layout="wide")
load_dotenv()
apply_custom_css()

# CACHING & STATE MANAGEMENT

@st.cache_resource(show_spinner="Loading AI Models...")
def get_agent(model_name, temperature, api_key):
    if api_key:
        os.environ["GROQ_API_KEY"] = api_key
    return CareerAI(model_name=model_name, temperature=temperature)

def init_session_state():
    defaults = {
        "resume_text": None, "job_desc": None, "analysis_result": None,
        "graph_data": None, "interview_q": None, "matched_keywords": [],
        "history": [], "company_context": "", "match_score": 0, "tailored_resume": None
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

init_session_state()

# UI COMPONENTS

def render_sidebar():
    with st.sidebar:
        c1, c2 = st.columns([1.5, 3])
        with c1: 
            st.image("img.webp", width=80)
        with c2: 
            st.markdown("<h2 style='margin: 5px 0 0 0; font-size: 1.2rem;'>CareerForge</h2>", unsafe_allow_html=True)
            st.caption("AI-Powered Architect")
        
        st.divider()
        st.markdown("### ⚙️ Control Panel")
        
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            api_key = st.text_input("🔑 Groq API Key", type="password", help="Get free key at console.groq.com")
            os.environ["GROQ_API_KEY"] = api_key if api_key else ""
        
        model = st.selectbox("🧠 AI Model", ["llama-3.3-70b-versatile", "llama-3.1-8b-instant"])
        persona = st.selectbox("🎭 Reviewer Persona", ["HR Recruiter", "Senior Engineer", "CTO"])
        temp = st.slider("🌡️ Creativity Level", 0.0, 1.0, 0.1)
        
        st.divider()
        st.markdown("### 🏢 Target Intelligence")
        company_name = st.text_input("Target Company", placeholder="e.g. Netflix, OpenAI")
        
        if st.session_state.history:
            st.divider()
            st.markdown("### 🕒 Recent Scans")
            for item in st.session_state.history[-3:]:
                 # Updated style for history items
                 st.markdown(f"""
                <div style='background: rgba(0, 243, 255, 0.05); border: 1px solid #333; padding: 8px; margin-bottom: 5px; font-size: 0.85rem;'>
                    <strong style='color: #eee;'>{item['company']}</strong> 
                    <span style='float: right; color: #00f3ff; font-family: monospace;'>{item['score']}%</span>
                </div>
                """, unsafe_allow_html=True)

        if st.session_state.analysis_result:
            st.divider()
            missing = st.session_state.graph_data.get('missing_skills', []) if st.session_state.graph_data else []
            pdf_file = create_pdf_report(
                name="Candidate", score=st.session_state.match_score, 
                analysis=st.session_state.analysis_result, missing_skills=missing
            )
            st.download_button("📄 Download Report PDF", pdf_file, "CareerForge_Report.pdf", "application/pdf")
            
        return model, temp, persona, company_name, api_key

def render_hero():
    # CYBERPUNK TITLE STYLE
    st.markdown("""
    <div style="text-align: center; margin-bottom: 40px;">
        <h1 style="font-size: 3.8rem; margin-bottom: 10px; 
            background: linear-gradient(to right, #00f3ff, #ff00ff); 
            -webkit-background-clip: text; 
            -webkit-text-fill-color: transparent;
            text-shadow: 0 0 20px rgba(0, 243, 255, 0.3);">
            CAREER FORGE <span style="font-size: 1.5rem; vertical-align: super; color: #555;">AI</span>
        </h1>
        <p style="font-size: 1.1rem; color: #00f3ff; letter-spacing: 2px; font-family: 'Roboto Mono', monospace;">
            Where AI Meets Ambition
        </p>
    </div>
    """, unsafe_allow_html=True)

def render_inputs():
    with st.container():
        # Metric card style is applied via CSS class 'metric-card'
        st.markdown("<div class='metric-card' style='text-align: left; padding: 30px;'>", unsafe_allow_html=True)
        c1, c2 = st.columns([1, 1], gap="large")
        with c1:
            st.markdown("#### 📄 Upload Resume")
            uploaded_file = st.file_uploader("Upload PDF", type=["pdf"], label_visibility="collapsed")
        with c2:
            st.markdown("#### 💼 Job Description")
            job_desc = st.text_area("Paste JD", height=150, label_visibility="collapsed", placeholder="Paste the job description here...")
        st.markdown("</div>", unsafe_allow_html=True)
    return uploaded_file, job_desc

# MAIN EXECUTION FLOW

model_name, temperature, persona_role, target_company, api_key = render_sidebar()
render_hero()
resume_file, job_description = render_inputs()

st.markdown("<br>", unsafe_allow_html=True)

# Analysis Logic
_, c2, _ = st.columns([1, 2, 1])
if c2.button("🔍 Analyze & Optimize Profile", type="primary", use_container_width=True):
    if not api_key:
        st.warning("⚠️ Please provide Groq API Key in the sidebar.")
    elif not resume_file or not job_description:
        st.warning("⚠️ Please provide both a Resume and Job Description.")
    else:
        with st.status("🚀 Launching CareerForge Analysis...", expanded=True) as status:
            try:
                agent = get_agent(model_name, temperature, api_key)
                status.write("📄 Extracting text from resume...")
                text = extract_text_from_pdf(resume_file)
                status.write(f"🏢 Researching {target_company if target_company else 'target company'}...")
                context = ""
                if target_company:
                    context = get_company_info(target_company)
                    if not context:
                        context = agent.generate_company_insight(target_company)
                st.session_state.company_context = context
                status.write("🧠 Performing semantic gap analysis...")
                agent.create_knowledge_base(text)
                score = agent.calculate_similarity(job_description)
                analysis = agent.analyze_profile(text, job_description, persona_role)
                
                st.session_state.resume_text = text
                st.session_state.job_desc = job_description
                st.session_state.match_score = score
                st.session_state.analysis_result = analysis
                st.session_state.graph_data = None 
                st.session_state.tailored_resume = None
                
                st.session_state.history.append({
                    "company": target_company if target_company else "Unknown",
                    "score": score
                })
                
                status.update(label="✅ Analysis Complete!", state="complete", expanded=False)
            except Exception as e:
                status.update(label="❌ Error Occurred", state="error")
                st.error(f"Analysis Failed: {str(e)}")

# RESULTS DASHBOARD
if st.session_state.analysis_result:
    st.divider()
    
    m1, m2, m3, m4 = st.columns(4)
    display_metric_card(m1, "Match Score", f"{st.session_state.match_score}%")
    display_metric_card(m2, "Word Count", len(st.session_state.resume_text.split()))
    display_metric_card(m3, "Persona", persona_role)
    display_metric_card(m4, "Company Intel", "Active" if st.session_state.company_context else "None")
    
    st.markdown("<br>", unsafe_allow_html=True)

    tabs = st.tabs([
        "📊 Analysis", "🔥 Heatmap", "🕸️ Skill Graph", "📝 Cover Letter", 
        "🎙️ Interview", "📧 Cold Email", "✍️ Rewrite", "🎓 Up-Skill"
    ])
    
    agent = get_agent(model_name, temperature, api_key)
    
    with tabs[0]:
        st.markdown("### 📑 AI Consultant Report")
        st.markdown(st.session_state.analysis_result)
        if st.session_state.company_context:
            st.info("💡 **Company Context Used:**")
            st.markdown(st.session_state.company_context)

    with tabs[1]:
        st.subheader("🔥 ATS Keyword Heatmap")
        if st.button("Generate Heatmap"):
            with st.spinner("Scanning..."):
                keywords = agent.extract_matched_keywords(st.session_state.resume_text, st.session_state.job_desc)
                st.session_state.matched_keywords = keywords
        
        if st.session_state.matched_keywords:
            pattern = re.compile(f"({'|'.join([re.escape(k) for k in st.session_state.matched_keywords])})", re.IGNORECASE)
            annotated_parts = []
            for part in pattern.split(st.session_state.resume_text):
                if part.lower() in [k.lower() for k in st.session_state.matched_keywords]:
                    # CHANGED COLOR FROM #8ef to #ff00ff (Neon Pink) to match theme
                    annotated_parts.append((part, "MATCH", "#ff00ff"))
                else:
                    annotated_parts.append(part)
            annotated_text(*annotated_parts)

    with tabs[2]:
        st.subheader("🕸️ Skill Gap Visualization")
        if st.button("Generate Graph"):
            with st.spinner("Mapping Skills..."):
                try:
                    json_str = agent.extract_skills_json(st.session_state.resume_text, st.session_state.job_desc)
                    st.session_state.graph_data = json.loads(json_str)
                except Exception as e:
                    st.error(f"Graph generation failed: {e}")
        
        if st.session_state.graph_data:
            nodes, edges, config = build_skill_graph(
                st.session_state.graph_data.get('present_skills', []), 
                st.session_state.graph_data.get('missing_skills', [])
            )
            agraph(nodes=nodes, edges=edges, config=config)

    with tabs[3]:
        st.subheader("📝 Cover Letter Generator")
        if st.button("Generate Cover Letter"):
            with st.spinner("Drafting..."):
                letter = agent.generate_cover_letter(st.session_state.resume_text, st.session_state.job_desc)
                st.text_area("Draft:", letter, height=400)
                st.download_button("📥 Download", letter, "Cover_Letter.txt")

    with tabs[4]:
        st.subheader("🎙️ AI Technical Interviewer")
        if st.button("Generate Question"):
            with st.spinner("Thinking..."):
                skills = ", ".join(st.session_state.graph_data.get('missing_skills', [])) if st.session_state.graph_data else "general gaps"
                st.session_state.interview_q = agent.generate_interview_question(st.session_state.job_desc, skills)
        
        if st.session_state.interview_q:
            st.markdown(f"**Q:** *{st.session_state.interview_q}*")
            audio = st.audio_input("Record Answer")
            if audio:
                with st.spinner("Grading..."):
                    text = agent.transcribe_audio(audio.read())
                    st.success(f"**You said:** {text}")
                    st.markdown(agent.evaluate_interview_answer(st.session_state.interview_q, text))

    with tabs[5]:
        st.subheader("📧 Networking Outreach")
        recipient = st.selectbox("Recipient", ["Hiring Manager", "Technical Recruiter", "Alumni / Peer"])
        if st.button("Draft Cold Email"):
            with st.spinner("Drafting..."):
                draft = agent.generate_cold_email(st.session_state.resume_text, st.session_state.job_desc, st.session_state.company_context, recipient)
                st.text_area("Draft:", draft, height=250)

    with tabs[6]:
        st.subheader("✍️ Resume Tailoring Studio")
        mode = st.radio("Mode:", ["Targeted Summary", "Full Resume Rewrite"], horizontal=True)
        
        if mode == "Targeted Summary":
            if st.button("✨ Rewrite Summary"):
                with st.spinner("Refining..."):
                    res = agent.llm.invoke(f"Rewrite resume summary for {target_company} job: {st.session_state.job_desc[:300]}... Original: {st.session_state.resume_text[:500]}").content
                    st.success(res)
        else:
            if st.button("🚀 Tailor Entire Resume"):
                with st.spinner("Optimizing..."):
                    try:
                        st.session_state.tailored_resume = agent.tailor_resume(st.session_state.resume_text, st.session_state.job_desc)
                    except AttributeError:
                        st.error("Error: `tailor_resume` not found in `src/llm_engine.py`.")
            
            if st.session_state.tailored_resume:
                st.divider()
                edited = st.text_area("Edit Result:", st.session_state.tailored_resume, height=500)
                st.download_button("📥 Download Markdown", edited, "Tailored_Resume.md")

    with tabs[7]:
        st.subheader("🚀 Accelerated Learning Plan")
        if st.button("Generate Roadmap"):
            with st.spinner("Planning & Finding Resources..."):
                skills = ", ".join(st.session_state.graph_data.get('missing_skills', [])) if st.session_state.graph_data else "General"
                
                # Generate learning plan
                roadmap = agent.generate_learning_plan(skills)
                st.markdown(roadmap)
                
                # Fetch YouTube tutorials for missing skills
                st.subheader("📺 Recommended YouTube Tutorials")
                missing_skills = st.session_state.graph_data.get('missing_skills', []) if st.session_state.graph_data else []
                
                if missing_skills:
                    for skill in missing_skills[:5]:  # Limit to first 5 skills
                        try:
                            # Search for YouTube tutorials
                            search_query = f"{skill} tutorial"
                            youtube_results = get_company_info(search_query)  # Reuse web search
                            
                            if youtube_results:
                                st.markdown(f"**{skill}**")
                                st.markdown(youtube_results)
                            else:
                                # Fallback: Create YouTube search link
                                youtube_link = f"https://www.youtube.com/results?search_query={skill.replace(' ', '+')}+tutorial"
                                st.markdown(f"**{skill}** - [Search YouTube →]({youtube_link})")
                        except Exception as e:
                            youtube_link = f"https://www.youtube.com/results?search_query={skill.replace(' ', '+')}+tutorial"
                            st.markdown(f"**{skill}** - [Search YouTube →]({youtube_link})")
                else:
                    st.info("No missing skills identified. You're all set!")
import os
import numpy as np
from langchain_core.prompts import PromptTemplate
from langchain_core.documents import Document
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from groq import Groq # Direct client for Audio

class CareerAI:
    def __init__(self, model_name="llama-3.3-70b-versatile", temperature=0.0):
        self.api_key = os.getenv("GROQ_API_KEY")
        self.llm = ChatGroq(
            temperature=temperature,
            model_name=model_name,
            api_key=self.api_key
        )
        self.embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        self.vector_db = None

    def create_knowledge_base(self, resume_text):
        if not resume_text: return
        chunks = [Document(page_content=chunk) for chunk in self._chunk_text(resume_text)]
        self.vector_db = FAISS.from_documents(chunks, self.embeddings)

    def _chunk_text(self, text, size=500):
        return [text[i:i+size] for i in range(0, len(text), size)]

    def calculate_similarity(self, job_desc):
        if not self.vector_db: return 0
        jd_embedding = self.embeddings.embed_query(job_desc)
        docs = self.vector_db.similarity_search(job_desc, k=5)
        if not docs: return 0
        doc_embeddings = [self.embeddings.embed_query(d.page_content) for d in docs]
        scores = [np.dot(jd_embedding, de) for de in doc_embeddings]
        return int(np.mean(scores) * 100)

    def analyze_profile(self, resume_text, job_desc, persona="HR Recruiter"):
        persona_prompts = {
            "HR Recruiter": "Focus on culture fit, soft skills, and red flags.",
            "Senior Engineer": "Focus strictly on technical depth, stack alignment, and complexity.",
            "CTO": "Focus on business value, ROI, and leadership potential."
        }
        instructions = persona_prompts.get(persona, "General analysis.")
        
        prompt = PromptTemplate(
            input_variables=["resume", "job_desc"],
            template=f"""
            Role: {persona}. Instructions: {instructions}
            JD: {{job_desc}}
            Resume: {{resume}}
            Task: detailed analysis, missing skills, score (0-100%). Output Markdown.
            """
        )
        return (prompt | self.llm).invoke({"resume": resume_text, "job_desc": job_desc}).content

    def extract_skills_json(self, resume_text, job_desc):
        prompt = PromptTemplate(
            input_variables=["resume", "job_desc"],
            template="""
            Extract skills. Return strictly JSON with keys: "present_skills" (list) and "missing_skills" (list).
            No markdown formatting.
            Resume: {resume}
            JD: {job_desc}
            """
        )
        res = (prompt | self.llm).invoke({"resume": resume_text, "job_desc": job_desc}).content
        return res.replace("```json", "").replace("```", "").strip()

    def generate_cover_letter(self, resume_text, job_desc):
        prompt = PromptTemplate(
            input_variables=["resume", "job_desc"],
            template="Write a professional cover letter. Resume: {resume}. JD: {job_desc}"
        )
        return (prompt | self.llm).invoke({"resume": resume_text, "job_desc": job_desc}).content

    # --- INTERVIEW FEATURES ---
    def generate_interview_question(self, job_desc, missing_skills):
        prompt = PromptTemplate(
            input_variables=["job_desc", "missing_skills"],
            template="Ask ONE hard technical interview question based on these missing skills: {missing_skills}. Job: {job_desc}."
        )
        return (prompt | self.llm).invoke({"job_desc": job_desc, "missing_skills": missing_skills}).content

    def evaluate_interview_answer(self, question, user_answer):
        prompt = PromptTemplate(
            input_variables=["question", "user_answer"],
            template="Grade this answer (0-10) and explain why. Question: {question}. Answer: {user_answer}."
        )
        return (prompt | self.llm).invoke({"question": question, "user_answer": user_answer}).content

    def transcribe_audio(self, audio_bytes):
        client = Groq(api_key=self.api_key)
        # Write temp file for the API
        with open("temp_audio.wav", "wb") as f:
            f.write(audio_bytes)
        with open("temp_audio.wav", "rb") as file:
            transcription = client.audio.transcriptions.create(
                file=("temp_audio.wav", file.read()),
                model="whisper-large-v3",
                response_format="json"
            )
        return transcription.text
    
    def extract_matched_keywords(self, resume_text, job_desc):
        """Finds keywords present in BOTH the resume and JD for highlighting."""
        prompt = PromptTemplate(
            input_variables=["resume", "job_desc"],
            template="""
            Identify the top 15 technical keywords or hard skills from the JD that are ALSO present in the Resume. 
            Return ONLY a comma-separated list of words. 
            Example Output: Python, SQL, AWS, Docker
            
            Resume: {resume}
            JD: {job_desc}
            """
        )
        res = (prompt | self.llm).invoke({"resume": resume_text, "job_desc": job_desc}).content
        # Clean list
        return [k.strip() for k in res.split(",") if k.strip()]
    

    def generate_cold_email(self, resume_text, job_desc, company_info, recipient="Hiring Manager"):
        prompt = PromptTemplate(
            input_variables=["resume", "job_desc", "company_info", "recipient"],
            template="""
            Write a high-converting Cold Email (max 150 words) to a {recipient}.
            
            Context:
            - Candidate Resume Summary: {resume}
            - Job Requirements: {job_desc}
            - Company News/Values: {company_info}
            
            Goal: Persuade them to accept a coffee chat or look at the application.
            Tone: Professional, concise, not desperate. Mention one specific alignment with their company news if relevant.
            """
        )
        return (prompt | self.llm).invoke({
            "resume": resume_text[:1000], 
            "job_desc": job_desc[:500], 
            "company_info": company_info,
            "recipient": recipient
        }).content
    


    def generate_company_insight(self, company_name):
        """Generates company insights using LLM internal training data (Fallback)."""
        prompt = PromptTemplate(
            input_variables=["company_name"],
            template="""
            You are a business intelligence analyst. 
            The user is applying to: {company_name}.
            
            Since live web search is unavailable, use your internal training data to provide:
            1. The company's likely Mission/Values.
            2. Their core Products or Services.
            3. The typical Tech Stack or technologies they use (if known).
            
            Format clearly with Markdown headers.
            Disclaimer: State that this is based on internal knowledge.
            """
        )
        return (prompt | self.llm).invoke({"company_name": company_name}).content
    

    def generate_learning_plan(self, missing_skills):
        prompt = PromptTemplate(
            input_variables=["missing_skills"],
            template="""
            The candidate is missing these skills: {missing_skills}.
            
            Task:
            1. Suggest ONE concrete "Weekend Project" idea that combines these specific skills.
            2. For each skill, provide a 1-sentence learning tip.
            
            Output in Markdown.
            """
        )
        return (prompt | self.llm).invoke({"missing_skills": missing_skills}).content
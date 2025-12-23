import os
import numpy as np
from langchain_core.prompts import PromptTemplate
from langchain_core.documents import Document
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

class CareerAI:
    def __init__(self, model_name="llama-3.3-70b-versatile", temperature=0.0):
        # 1. Initialize LLM with dynamic settings
        api_key = os.getenv("GROQ_API_KEY")
        self.llm = ChatGroq(
            temperature=temperature,
            model_name=model_name,
            api_key=api_key
        )
        
        # 2. Initialize Embeddings (Updated for LangChain 0.2+)
        self.embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        self.vector_db = None

    def create_knowledge_base(self, resume_text):
        """Creates a temporary vector store from the resume content."""
        if not resume_text: return
        chunks = [Document(page_content=chunk) for chunk in self._chunk_text(resume_text)]
        self.vector_db = FAISS.from_documents(chunks, self.embeddings)

    def _chunk_text(self, text, size=500):
        return [text[i:i+size] for i in range(0, len(text), size)]

    def calculate_similarity(self, job_desc):
        """Calculates semantic similarity score (0-100)."""
        if not self.vector_db: return 0
        jd_embedding = self.embeddings.embed_query(job_desc)
        docs = self.vector_db.similarity_search(job_desc, k=5)
        if not docs: return 0
        doc_embeddings = [self.embeddings.embed_query(d.page_content) for d in docs]
        scores = [np.dot(jd_embedding, de) for de in doc_embeddings]
        return int(np.mean(scores) * 100)

    def analyze_profile(self, resume_text, job_desc):
        """Full LLM analysis pipeline."""
        prompt = PromptTemplate(
            input_variables=["resume", "job_desc"],
            template="""
            You are an expert ATS (Applicant Tracking System) and Career Coach.
            JOB DESCRIPTION: {job_desc}
            CANDIDATE RESUME: {resume}
            
            Task:
            1. Analyze the semantic match.
            2. Identify 3 missing Hard Skills & 3 Soft Skills.
            3. Provide a "Tone Analysis".
            4. Give a "Hiring Probability" score (0-100%).
            Output strictly in Markdown.
            """
        )
        return (prompt | self.llm).invoke({"resume": resume_text, "job_desc": job_desc}).content

    def generate_cover_letter(self, resume_text, job_desc):
        prompt = PromptTemplate(
            input_variables=["resume", "job_desc"],
            template="""
            Write a persuasive cover letter for this candidate.
            Resume: {resume}
            JD: {job_desc}
            """
        )
        return (prompt | self.llm).invoke({"resume": resume_text, "job_desc": job_desc}).content
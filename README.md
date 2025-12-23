# 🚀 CareerForge AI

**CareerForge AI** is an intelligent career optimization platform powered by **Llama-3** and **Groq**. It helps job seekers bridge the gap between their resume and their dream job using advanced RAG (Retrieval Augmented Generation), live company intelligence, and interactive skill visualization.

## ✨ Features

- **📄 AI Resume Analysis**: Detailed feedback tailored to specific personas (HR Recruiter, Senior Engineer, CTO).
- **📊 Match Scoring**: Semantic similarity calculation using vector embeddings.
- **🕸️ Interactive Skill Graph**: Visualizes skill gaps (Green = Has, Red = Missing).
- **🏢 Company Intelligence**: Scrapes live web data to fetch company values, news, and tech stack.
- **🎙️ AI Mock Interview**: Audio-based technical interview simulator with speech-to-text grading.
- **🔥 ATS Heatmap**: Highlights keywords in your resume that match the job description.
- **📥 PDF Reports**: Generates a downloadable, professional analysis report.

## 🛠️ Tech Stack

- **Frontend**: Streamlit
- **LLM Engine**: Groq API (Llama-3.3-70b), LangChain
- **Embeddings & RAG**: HuggingFace (`all-MiniLM-L6-v2`), FAISS
- **Search**: DuckDuckGo Search
- **Visualization**: Streamlit Agraph
- **Audio**: OpenAI Whisper (via Groq)

## ⚙️ Installation

1. **Clone the repository**
   ```bash
   git clone [https://github.com/yourusername/careerforge-ai.git](https://github.com/yourusername/careerforge-ai.git)
   cd careerforge-ai
2. **Create a virtual environment**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate

3. **Install dependencies**
  ```bash
  pip install -r requirements.txt

import pdfplumber
import re

def extract_text_from_pdf(file_path):
    """Extracts text from uploaded PDF file."""
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return clean_text(text)

def clean_text(text):
    """Basic text cleaning to remove artifacts."""
    text = re.sub(r'\s+', ' ', text)  # Remove extra whitespace
    text = re.sub(r'[^\x00-\x7F]+', ' ', text)  # Remove non-ASCII
    return text.strip()
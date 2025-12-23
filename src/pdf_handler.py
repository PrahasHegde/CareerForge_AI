import pdfplumber
import re

def extract_text_from_pdf(file):
    """Extracts clean text from a PDF file object."""
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return _clean_text(text)

def _clean_text(text):
    """Internal helper to clean whitespace and artifacts."""
    text = re.sub(r'\s+', ' ', text)  # Remove extra whitespace
    text = re.sub(r'[^\x00-\x7F]+', ' ', text)  # Remove non-ASCII
    return text.strip()
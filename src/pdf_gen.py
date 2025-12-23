from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.utils import simpleSplit
import io

def create_pdf_report(name, score, analysis, missing_skills):
    """Generates a PDF report in memory."""
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    
    # 1. Header
    c.setFillColorRGB(0.1, 0.2, 0.5) # Navy Blue
    c.rect(0, height - 100, width, 100, fill=1, stroke=0)
    
    c.setFillColorRGB(1, 1, 1) # White text
    c.setFont("Helvetica-Bold", 24)
    c.drawString(50, height - 60, "CareerForge AI Analysis")
    
    c.setFont("Helvetica", 14)
    c.drawString(50, height - 85, f"Candidate Report for: {name}")

    # 2. Score Section
    c.setFillColorRGB(0, 0, 0) # Black
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 140, f"Match Score: {score}%")
    
    # 3. Missing Skills
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, height - 170, "Identified Gaps / Missing Skills:")
    
    c.setFont("Helvetica", 10)
    c.setFillColorRGB(0.8, 0.1, 0.1) # Red for gaps
    skills_text = ", ".join(missing_skills) if missing_skills else "None detected."
    c.drawString(50, height - 185, skills_text)
    
    # 4. Detailed Analysis Body
    c.setFillColorRGB(0, 0, 0)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, height - 220, "Detailed AI Feedback:")
    
    c.setFont("Helvetica", 10)
    text_y = height - 240
    
    # Wrap text to fit page
    lines = analysis.split('\n')
    for paragraph in lines:
        # Split long lines into smaller chunks that fit width
        wrapped_lines = simpleSplit(paragraph, "Helvetica", 10, width - 100)
        for line in wrapped_lines:
            if text_y < 50: # New Page if at bottom
                c.showPage()
                text_y = height - 50
                c.setFont("Helvetica", 10)
            
            c.drawString(50, text_y, line)
            text_y -= 14 # Line spacing
        text_y -= 10 # Paragraph spacing

    c.save()
    buffer.seek(0)
    return buffer
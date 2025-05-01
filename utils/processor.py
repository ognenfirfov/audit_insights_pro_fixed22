from openai import OpenAI
import fitz  # PyMuPDF
import os

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def extract_text(pdf_path):
    """Extract text from a PDF file using PyMuPDF."""
    doc = fitz.open(pdf_path)
    return "\n".join(page.get_text() for page in doc)

def summarize_audit(text):
    """Summarize key elements of a single audit using AI."""
    prompt = f"""You are an auditor. Analyze the following audit report and summarize:
- Key Findings
- Measures Taken
- Key Issues
- Notable Outcomes

Report:
{text}

Return a clear, bullet-point or structured summary.
"""
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )
    return response.choices[0].message.content

def compare_audits(summaries):
    """Use AI to compare multiple audit summaries."""
    joined = "\n\n".join(f"Audit {i+1}:\n{summary}" for i, summary in enumerate(summaries))
    prompt = f"""You are a senior auditor. Compare the following summaries:

{joined}

Highlight:
- Similarities
- Differences
- Common problems and solutions

Return a clear, structured comparison.
"""
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )
    return response.choices[0].message.content

def extract_learnings(summaries):
    """Generate learnings or best practices from audit summaries."""
    joined = "\n\n".join(summaries)
    prompt = f"""From the following audit summaries, extract 3–5 key learnings or best practices that could improve future audits:

{joined}
"""
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )
    return response.choices[0].message.content

def analyze_audits(paths):
    """Main function: Analyze all

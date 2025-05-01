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
    prompt = (
        "You are an auditor. Analyze the following audit report and summarize:\n"
        "- Key Findings\n"
        "- Measures Taken\n"
        "- Key Issues\n"
        "- Notable Outcomes\n\n"
        f"Report:\n{text}\n\n"
        "Return a clear, bullet-point or structured summary."
    )
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )
    return response.choices[0].message.content

def compare_audits(summaries):
    """Use AI to compare multiple audit summaries."""
    joined = "\n\n".join(f"Audit {i+1}:\n{summary}" for i, summary in enumerate(summaries))
    prompt = (
        "You are a senior auditor. Compare the following summaries:\n\n"
        f"{joined}\n\n"
        "Highlight:\n"
        "- Similarities\n"
        "- Differences\n"
        "- Common problems and solutions\n\n"
        "Return a clear, structured comparison."
    )
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )
    return response.choices[0].message.content

def extract_learnings(summaries):
    """Generate learnings or best practices from audit summaries."""
    joined = "\n\n".join(summaries)
    prompt = (
        "From the following audit summaries, extract 3–5 key learnings or best practices "
        "that could improve future audits:\n\n"
        f"{joined}"
    )
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )
    return response.choices[0].message.content

def analyze_audits(paths):
    """Main function: Analyze all uploaded audits and return summaries, comparison, and learnings."""
    summaries = [summarize_audit(extract_text(path)) for path in paths]
    comparison = compare_audits(summaries)
    learnings = extract_learnings(summaries)
    return summaries, comparison, learnings


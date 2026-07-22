import fitz  # PyMuPDF
import docx

# -----------------------------
# PDF Reader
# -----------------------------
def extract_pdf_text(uploaded_file):
    text = ""

    pdf = fitz.open(stream=uploaded_file.read(), filetype="pdf")

    for page in pdf:
        text += page.get_text()

    return text


# -----------------------------
# DOCX Reader
# -----------------------------
def extract_docx_text(uploaded_file):

    text = ""

    doc = docx.Document(uploaded_file)

    for para in doc.paragraphs:
        text += para.text + "\n"

    return text


# -----------------------------
# Main Function
# -----------------------------
def extract_resume(uploaded_file):

    if uploaded_file is None:
        return ""

    if uploaded_file.name.endswith(".pdf"):
        return extract_pdf_text(uploaded_file)

    elif uploaded_file.name.endswith(".docx"):
        return extract_docx_text(uploaded_file)

    return ""

def extract_candidate_name(resume_text):

    lines = resume_text.split("\n")

    for line in lines:

        line = line.strip()

        if not line:
            continue

        if (
            "b.tech" in line.lower()
            or "computer science" in line.lower()
            or "email" in line.lower()
            or "phone" in line.lower()
            or "mobile" in line.lower()
            or "resume" in line.lower()
        ):
            continue

        words = line.split()

        if 2 <= len(words) <= 4:
            return line

    return "Candidate"
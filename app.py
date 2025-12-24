import os
import zipfile
import tempfile
import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from typing import TypedDict, List
import re

from PyPDF2 import PdfReader
from docx import Document



load_dotenv()


class ResumeSchema(TypedDict):
    name: str
    email: str
    phone: str
    skills: List[str]
    education: str
    experience_summary: str
    linkedin: str
    github: str


def find_email(text: str) -> str:
    m = re.search(r"[\w\.-]+@[\w\.-]+", text)
    return m.group(0) if m else ""


def find_phone(text: str) -> str:
    m = re.search(r"(\+?\d[\d\-\s()]{7,}\d)", text)
    return m.group(0).strip() if m else ""


def find_links(text: str, domain: str) -> str:
    m = re.search(rf"https?://[\w./-]*{re.escape(domain)}[\w./-]*", text, re.IGNORECASE)
    return m.group(0) if m else ""


def find_skills(text: str) -> List[str]:
    # Look for a Skills section, otherwise return top candidate keywords
    skills_section = re.search(r"Skills[:\n\r]+([\s\S]{0,200})", text, re.IGNORECASE)
    if skills_section:
        candidates = re.split(r"[,;\n\r\\/|]", skills_section.group(1))
        return [s.strip() for s in candidates if s.strip()][:20]

    # fallback: find common skill keywords
    common = ["python","javascript","sql","aws","docker","kubernetes",
              "react","node","pandas","tensorflow","excel"]
    found = [w for w in common if re.search(rf"\b{w}\b", text, re.IGNORECASE)]
    return found


def summarize_experience(text: str) -> str:
    # crude summary: take the first 3 non-empty paragraphs after header
    parts = [p.strip() for p in re.split(r"\n{2,}", text) if p.strip()]
    if len(parts) >= 2:
        return " ".join(parts[1:3])[:800]
    return parts[0][:800] if parts else ""


def find_education(text: str) -> str:
    # Try to find an Education section block
    m = re.search(r"Education[:\n\r]+([\s\S]{0,400})", text, re.IGNORECASE)
    if m:
        content = m.group(1)
        # stop at common section headers
        content = re.split(r"\n{2,}|Experience[:\n\r]|Skills[:\n\r]|LinkedIn[:\n\r]|GitHub[:\n\r]", content)[0]
        return " ".join(line.strip() for line in content.splitlines() if line.strip())[:800]

    # fallback: find common degree / university mentions
    m2 = re.search(r"(B\.?Sc|M\.?Sc|Bachelor|Master|Ph\.?D|University|College)[^\n]{0,200}", text, re.IGNORECASE)
    return m2.group(0).strip() if m2 else ""
def read_pdf(file_path):
    reader = PdfReader(file_path)
    return "\n".join(page.extract_text() or "" for page in reader.pages)

def read_docx(file_path):
    doc = Document(file_path)
    return "\n".join(p.text for p in doc.paragraphs)


def process_resume(text):
    # Implement local parsing logic here
    email = find_email(text)
    phone = find_phone(text)
    skills = find_skills(text)
    education = find_education(text)
    linkedin = find_links(text, "linkedin.com")
    github = find_links(text, "github.com")
    experience_summary = summarize_experience(text)

    return ResumeSchema(
        name="",  # Placeholder, implement name extraction if needed
        email=email,
        phone=phone,
        skills=skills,
        experience_summary=experience_summary,
        education=education,
        linkedin=linkedin,
        github=github
    )


def main():
    st.set_page_config(page_title="AI Resume Analyzer", layout="centered")

    st.title("📄 AI-Powered Resume Analyzer & CSV Generator")
    st.write("Upload a ZIP file containing resumes (PDF / DOCX)")

    uploaded_zip = st.file_uploader("Upload ZIP file", type=["zip"])

    if uploaded_zip:
        with tempfile.TemporaryDirectory() as temp_dir:
            zip_path = os.path.join(temp_dir, "resumes.zip")

            with open(zip_path, "wb") as f:
                f.write(uploaded_zip.read())

            with zipfile.ZipFile(zip_path, "r") as zip_ref:
                zip_ref.extractall(temp_dir)

            results = []

            for root, _, files in os.walk(temp_dir):
                for file in files:
                    file_path = os.path.join(root, file)

                    if file.endswith(".pdf"):
                        text = read_pdf(file_path)

                    elif file.endswith(".docx"):
                        text = read_docx(file_path)

                    else:
                        continue

                    if text.strip():
                        try:
                            data = process_resume(text)
                            results.append(data)
                        except Exception as e:
                            st.error(f"Error processing {file}: {e}")

            if results:
                df = pd.DataFrame(results)
                st.success("✅ Resume analysis completed!")

                st.dataframe(df)

                csv = df.to_csv(index=False).encode("utf-8")
                st.download_button(
                    label="⬇️ Download CSV",
                    data=csv,
                    file_name="resume_analysis.csv",
                    mime="text/csv"
                )
            else:
                st.warning("No valid resumes found.")


if __name__ == "__main__":
    main()
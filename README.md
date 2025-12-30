# AI-Powered-Resume-Analyzer

An AI-driven application that automatically analyzes resumes in bulk and converts unstructured resume content into a structured CSV file.
Built using Streamlit and LangChain, this project demonstrates how Large Language Models (LLMs) can be applied to real-world HR and recruitment workflows.

[![Live App](https://img.shields.io/badge/Live%20App-Streamlit-red?style=for-the-badge&logo=streamlit)](https://ai-powered-resume-analyzer-slzknhcqymcjgoudarizvl.streamlit.app/)

🔍 Project Overview

Recruiters and HR teams often receive resumes in bulk, usually as ZIP files containing multiple resumes in PDF or DOCX format.
Manually extracting candidate details from each resume is time-consuming, inconsistent, and error-prone.

This application automates the entire process by:

🔹Reading resumes from a ZIP file
🔹Extracting key information using an AI model
🔹Converting unstructured resume text into structured data
🔹Generating a downloadable CSV file for easy analysis

✅ Key Features
📦 Upload a ZIP file containing multiple resumes (PDF / DOCX)
🧠 AI-powered resume understanding using LLMs
🧾 Extracts structured fields such as:
Name
Email
Phone
Skills
Experience Summary
LinkedIn
GitHub
📊 Displays extracted data in a table
📥 Download results as a CSV file
⚡ Handles nested folders inside ZIP files
🛡 Graceful handling of API rate limits
🧑‍🎓 Beginner-friendly, readable codebase

🧩Tech Stack
Streamlit
LangChain
Google Gemini
PyPDF2, python-docx
zipfile
docx

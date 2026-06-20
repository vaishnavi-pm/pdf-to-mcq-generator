import os
import streamlit as st
import fitz
from google import genai

# -----------------------------
# Gemini API Key
# -----------------------------

API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=API_KEY)

# -----------------------------
# Streamlit UI
# -----------------------------

st.title("📘 PDF to MCQ Generator")

st.write(
    "Upload a PDF and generate 20 MCQs using Gemini AI."
)

uploaded_file = st.file_uploader(
    "Upload PDF",
    type=["pdf"]
)

if uploaded_file is not None:

    st.success("PDF Uploaded Successfully!")

    # Read PDF

    pdf_bytes = uploaded_file.read()

    doc = fitz.open(
        stream=pdf_bytes,
        filetype="pdf"
    )

    text = ""

    for page in doc:

        text += page.get_text()

    doc.close()

    st.success("Text Extracted Successfully!")

    if st.button("Generate MCQs"):

        with st.spinner("Generating MCQs..."):

            prompt = f"""
Generate 20 Multiple Choice Questions (MCQs) from the following text.

Rules:

1. Each question should have 4 options.

2. Only one option should be correct.

3. Mention the correct answer.

4. Questions should be medium to hard level.

5. Format:

Q1. Question

A. Option 1

B. Option 2

C. Option 3

D. Option 4

Answer: A

Text:

{text[:15000]}
"""

            try:

                response = client.models.generate_content(

                    model="gemini-2.5-flash",

                    contents=prompt

                )

                st.subheader("Generated MCQs")

                st.write(response.text)

            except Exception as e:

                st.error(f"Error: {e}")

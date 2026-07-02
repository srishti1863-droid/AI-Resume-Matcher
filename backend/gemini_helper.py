import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-2.5-flash")


def generate_feedback(resume_text, job_description):
    prompt = f"""
You are an ATS Resume Reviewer.

Analyze the following resume and compare it with the given job description.

Resume:
{resume_text}

Job Description:
{job_description}

Provide:
1. Overall feedback.
2. Strengths.
3. Missing skills.
4. Suggestions to improve the resume.

Keep the response concise and use bullet points.
"""

    response = model.generate_content(prompt)

    return response.text
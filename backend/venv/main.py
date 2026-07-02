from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import os
import shutil
import fitz

from models import JobDescription
from matcher import calculate_match
from skill_extractor import extract_skills
from ats_score import calculate_ats_score
from gemini_helper import generate_feedback
import resume_data

app = FastAPI(title="AI Resume Matcher API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.get("/")
def home():
    return {"message": "Welcome to AI Resume Matcher API 🚀"}


@app.post("/upload-resume")
async def upload_resume(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    doc = fitz.open(file_path)

    text = ""
    for page in doc:
        text += page.get_text()

    doc.close()

    found_skills = extract_skills(text)

    resume_data.resume_skills = found_skills
    resume_data.resume_text = text

    return {
        "message": "Resume uploaded successfully",
        "filename": file.filename,
        "skills": found_skills
    }


@app.post("/match-resume")
def match_resume(job: JobDescription):

    job_skills = extract_skills(job.description)

    result = calculate_match(
        resume_data.resume_skills,
        job_skills
    )

    ats_score = calculate_ats_score(
        resume_data.resume_text,
        result["matched_skills"],
        job_skills
    )

    ai_feedback = generate_feedback(
        resume_data.resume_text,
        job.description
    )

    result["ats_score"] = ats_score
    result["ai_feedback"] = ai_feedback

    return result
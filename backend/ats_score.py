import re

def calculate_ats_score(resume_text, matched_skills, job_skills):

    score = 0

    # ---------- Skill Match (40 Marks) ----------
    if len(job_skills) > 0:
        score += (len(matched_skills) / len(job_skills)) * 40

    # ---------- Email (5 Marks) ----------
    if re.search(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", resume_text):
        score += 5

    # ---------- Phone (5 Marks) ----------
    if re.search(r"\+?\d[\d\s\-]{8,}", resume_text):
        score += 5

    # ---------- GitHub (10 Marks) ----------
    if "github" in resume_text.lower():
        score += 10

    # ---------- LinkedIn (10 Marks) ----------
    if "linkedin" in resume_text.lower():
        score += 10

    # ---------- Projects (15 Marks) ----------
    if "project" in resume_text.lower():
        score += 15

    # ---------- Education (10 Marks) ----------
    education_keywords = [
        "b.tech",
        "btech",
        "bachelor",
        "degree",
        "university",
        "college"
    ]

    for word in education_keywords:
        if word in resume_text.lower():
            score += 10
            break

    # ---------- Resume Length (5 Marks) ----------
    if len(resume_text.split()) >= 250:
        score += 5

    return round(min(score, 100), 2)
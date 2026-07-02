def calculate_match(resume_skills, job_skills):

    matched_skills = []
    missing_skills = []
    suggestions = []

    for skill in job_skills:
        if skill in resume_skills:
            matched_skills.append(skill)
        else:
            missing_skills.append(skill)

    if len(job_skills) == 0:
        match_percentage = 0
    else:
        match_percentage = round(
            (len(matched_skills) / len(job_skills)) * 100,
            2
        )

    # Generate resume suggestions
    if len(missing_skills) > 0:
        for skill in missing_skills:
            suggestions.append(f"Add {skill} to your resume if you have experience with it.")

    if match_percentage >= 90:
        suggestions.append("Excellent! Your resume is highly relevant to this job.")
    elif match_percentage >= 70:
        suggestions.append("Good match. Improve the missing skills to increase your chances.")
    elif match_percentage >= 50:
        suggestions.append("Your resume is a moderate match. Consider adding more relevant projects and skills.")
    else:
        suggestions.append("Your resume needs significant improvements for this job role.")

    suggestions.append("Use action verbs like Developed, Designed, Implemented, Optimized.")
    suggestions.append("Add measurable achievements (e.g., Improved performance by 30%).")

    return {
        "match_percentage": match_percentage,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "suggestions": suggestions
    }
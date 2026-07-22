import json
import os
import re


# ----------------------------
# Load Skills Database
# ----------------------------
def load_skills():

    path = os.path.join("data", "skills_database.json")

    with open(path, "r") as file:
        data = json.load(file)

    return data["skills"]


# ----------------------------
# Extract Skills
# ----------------------------
def extract_skills(text):

    text = text.lower()

    skills = load_skills()

    found = []

    for skill in skills:

        if skill.lower() in text:

            found.append(skill)

    return sorted(list(set(found)))


# ----------------------------
# ATS Score
# ----------------------------
def calculate_ats_score(resume_text, job_description):

    resume_skills = extract_skills(resume_text)

    jd_skills = extract_skills(job_description)

    matched = list(set(resume_skills) & set(jd_skills))

    missing = list(set(jd_skills) - set(resume_skills))

    if len(jd_skills) == 0:
        score = 0
    else:
        score = round((len(matched) / len(jd_skills)) * 100)

    return {
        "score": score,
        "matched": sorted(matched),
        "missing": sorted(missing)
    }
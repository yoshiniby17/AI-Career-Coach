from modules.groq_client import client


def generate_cover_letter(resume, job_description):

    prompt = f"""
You are an expert career coach and professional resume writer.

Create a unique and personalized cover letter.

Candidate Resume:
{resume}


Job Description:
{job_description}


Rules:
- Do NOT use a fixed template.
- Every cover letter must be different based on the candidate resume.
- Analyze candidate skills, projects, education and experience.
- Match skills with job requirements.
- Mention relevant projects only from resume.
- Avoid fake information.
- Make it suitable for ATS.
- Professional but human tone.
- 4 to 5 paragraphs only.

Structure:

1. Professional greeting
2. Introduction about candidate and role interest
3. Technical skills and project achievements matching JD
4. Why candidate fits this company
5. Closing statement


Generate only the cover letter.
"""


    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role":"system",
                "content":
                "You are a senior HR recruiter and career advisor."
            },
            {
                "role":"user",
                "content":prompt
            }
        ],
        temperature=0.8,
        max_tokens=1200
    )


    return response.choices[0].message.content
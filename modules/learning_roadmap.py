from modules.groq_client import client

def generate_learning_roadmap(resume, jd):

    prompt = f"""
You are an AI Career Mentor.

Based on the Resume and Job Description, generate a professional learning roadmap.

Include:

1. Current Skill Level
2. Missing Skills
3. 12 Week Learning Plan
4. Projects
5. Certifications
6. Interview Preparation
7. Final Career Advice

Resume:
{resume}

Job Description:
{jd}
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content
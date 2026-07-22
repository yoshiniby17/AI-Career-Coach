from modules.groq_client import client

def analyze_resume(resume_text, job_description):

    prompt = f"""
You are an expert ATS Resume Analyzer.

Analyze the following resume against the given Job Description.

Resume:
{resume_text}

Job Description:
{job_description}

Return your response in this format:

1. Resume Summary
2. Skills Found
3. Missing Skills
4. Strengths
5. Weaknesses
6. Suggestions
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "system",
                "content": "You are a professional ATS Resume Analyzer."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.3
    )

    return response.choices[0].message.content
from modules.groq_client import client

SYSTEM_PROMPT = """
You are a Senior Technical Interviewer with 15+ years of experience.

You are conducting a REAL interview.

Rules:

1. Ask ONLY one interview question at a time.

2. Wait for the candidate's answer.

3. Never answer interview questions.

4. Never explain technical concepts.

5. If the candidate asks for an answer or asks any technical question, always reply:

'As the interviewer, I cannot answer interview questions. Please answer using your own knowledge.'

6. Even if the candidate asks multiple times, never reveal the answer.

7. Stay professional.

8. Continue the interview until it ends.

9. Use the Resume and Job Description as interview context.
"""


def create_history(resume, jd):

    history = [

        {
            "role": "system",
            "content": SYSTEM_PROMPT
        },

        {
            "role": "system",
            "content": f"""
Candidate Resume:

{resume}

Job Description:

{jd}

Start the interview.
Ask only ONE question.
"""
        }

    ]

    return history


def interview_chat(history):

    response = client.chat.completions.create(

        model="llama-3.1-8b-instant",

        messages=history,

        temperature=0.3

    )

    return response.choices[0].message.content

def analyze_interview(resume, jd, history):

    prompt = f"""
You are a Senior HR Interview Evaluator.

Analyze the complete interview based on:

Resume:
{resume}

Job Description:
{jd}

Interview Conversation:
{history}

Evaluate the candidate and return ONLY in the following format:

Overall Score: XX/100

Communication: XX/100

Confidence: XX/100

Technical Knowledge: XX/100

Problem Solving: XX/100

Strengths:
- Point 1
- Point 2
- Point 3

Weaknesses:
- Point 1
- Point 2
- Point 3

Final Feedback:
Write a professional paragraph (4-5 lines) summarizing the interview performance.

Do not use markdown.
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "system",
                "content": "You are an expert HR Interview Evaluator."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2
    )

    return response.choices[0].message.content
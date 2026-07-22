import streamlit as st
import os
from modules.resume_parser import (
    extract_resume,
    extract_candidate_name
)
from modules.resume_analysis import analyze_resume
from modules.ats_score import calculate_ats_score
from modules.skill_matcher import calculate_jd_match
from modules.groq_client import client
import time


if "resume_file" not in st.session_state:
    st.session_state.resume_file = None

if "resume_name" not in st.session_state:
    st.session_state.resume_name = ""

if "job_description" not in st.session_state:
    st.session_state.job_description = ""

if "interview_analysis" not in st.session_state:
    st.session_state.interview_analysis = ""
    
if "interview_start_time" not in st.session_state:
    st.session_state.interview_start_time = None
# -------------------------------
# PAGE CONFIG
# -------------------------------
st.set_page_config(
    page_title="AI Career Coach",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
    
)

# -------------------------------
# LOAD CSS
# -------------------------------
css_path = os.path.join("assets", "style.css")

if os.path.exists(css_path):
    with open(css_path) as f:
        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True
        )

# -------------------------------
# SESSION STATE
# -------------------------------

default_states = {
    "resume_text": "",
    "job_description": "",
    "resume_analysis": "",
    "ats_score": 0,
    "jd_match": 0,
    "missing_skills": [],
    "questions": [],
    "answers": [],
    "feedback": "",
    "cover_letter": "",
    "roadmap": "",
    "report": ""
}

for key, value in default_states.items():
    if key not in st.session_state:
        st.session_state[key] = value

# -------------------------------
# SIDEBAR
# -------------------------------

# Logo (Optional)
# st.sidebar.image("assets/logo.png", width=120)

st.sidebar.title("🤖 AI Career Coach")

st.sidebar.title("AI Career Coach")

page = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Dashboard",
        "📄 Resume Analysis",
        "📊 ATS Score",
        "🎯 JD Matching",
        "🎤 AI Interview",
        "📝 Cover Letter",
        "📚 Learning Roadmap",
        "📑 Final Report"
    ]
)

# -------------------------------
# DASHBOARD
# -------------------------------

if page == "🏠 Dashboard":

    st.markdown(
        "<h1 class='main-title'>🤖 AI Career Coach & Resume Tailor</h1>",
        unsafe_allow_html=True
    )

    st.write("")

    col1, col2 = st.columns(2)

    with col1:

        st.markdown("""
        <div class="card">
        <h3>🚀 Features</h3>

        ✔ Resume Upload

        ✔ Resume Analysis

        ✔ ATS Score

        ✔ JD Matching

        ✔ AI Interview

        ✔ Cover Letter

        ✔ Learning Roadmap

        ✔ Final Report
        </div>
        """, unsafe_allow_html=True)

    with col2:

        st.markdown("""
        <div class="card">
        <h3>🎯 Project Goal</h3>

        Upload Resume

        ↓

        Upload Job Description

        ↓

        AI Analysis

        ↓

        ATS Score

        ↓

        AI Interview

        ↓

        Hiring Recommendation
        </div>
        """, unsafe_allow_html=True)

    st.write("")

    st.info("👈 Select a module from the left sidebar.")


# -------------------------------
# RESUME ANALYSIS
# -------------------------------

elif page == "📄 Resume Analysis":

    st.title("📄 Resume Analysis")

    st.subheader("Upload Resume")

    resume = st.file_uploader(
        "Upload Resume",
        type=["pdf", "docx"],
        key="resume_upload"
    )


    if resume is not None:

        st.session_state.resume_file = resume
        st.session_state.resume_name = resume.name


    if st.session_state.resume_file is not None:

        resume = st.session_state.resume_file


    if st.session_state.resume_name:

        st.success(
            f"📄 Uploaded Resume: {st.session_state.resume_name}"
        )


        st.subheader("Paste Job Description")


        job_description = st.text_area(
            "Job Description",
            height=250,
            key="jd_input",
            value=st.session_state.job_description
        )


        st.session_state.job_description = job_description


        if st.button("Analyze Resume"):


            if resume is None:

                st.warning("Please upload resume.")


            elif job_description.strip() == "":

                st.warning("Please paste Job Description.")


            else:

                resume_text = extract_resume(resume)
                st.code(resume_text[:500])

                st.session_state.candidate_name = extract_candidate_name(resume_text)
                st.session_state.resume_text = resume_text


                with st.spinner("Analyzing Resume..."):

                    analysis = analyze_resume(
                        resume_text,
                        job_description
                    )

                    ats = calculate_ats_score(
                        resume_text,
                        job_description
                    )
                    
                    st.write(ats)
                
                    match_score = calculate_jd_match(
                    resume_text,
                    job_description
                    )

                st.session_state.jd_match_score = match_score

                st.session_state.resume_analysis = analysis
                st.session_state.ats_score = ats


                st.success("✅ Resume analyzed successfully.")


    # Always show Resume Analysis
    if st.session_state.get("resume_analysis"):

        st.divider()

        st.subheader("📄 Resume Analysis")

        st.write(st.session_state.resume_analysis)
                
# -------------------------------
# ATS
# -------------------------------

elif page == "📊 ATS Score":

    st.title("📊 ATS Score")

    ats = st.session_state.get("ats_score", None)

    if ats is None or ats == 0:
        st.warning("⚠ Please analyze your resume first.")

    else:

        st.progress(ats["score"] / 100)

        st.metric(
            "ATS Score",
            f"{ats['score']}%"
        )

        col1, col2 = st.columns(2)

        with col1:

            st.success("✅ Matched Skills")

            if ats["matched"]:
                st.write(", ".join(ats["matched"]))
            else:
                st.write("No matched skills found.")

        with col2:

            st.error("❌ Missing Skills")

            if ats["missing"]:
                st.write(", ".join(ats["missing"]))
            else:
                st.write("No missing skills.")
                
            
# -------------------------------
# JD MATCH
# -------------------------------

elif page == "🎯 JD Matching":

    st.title("🎯 JD Matching")

    if "jd_match_score" not in st.session_state:
        st.warning("⚠ Please analyze your resume first.")

    else:
        st.subheader("📊 JD Match Score")

        st.progress(st.session_state.jd_match_score / 100)

        st.metric(
            "JD Match Score",
            f"{st.session_state.jd_match_score}%"
        )

        st.success(
            f"Your resume matches {st.session_state.jd_match_score}% with the Job Description."
        )

# -------------------------------
# INTERVIEW
# -------------------------------
elif page == "🎤 AI Interview":

    from modules.interview_chatbot import (
        create_history,
        interview_chat,
        analyze_interview
    )

    st.title("🎤 AI Interview")

    if st.session_state.resume_text == "":
        st.warning("⚠ Please analyze your resume first.")
        st.stop()

    if st.session_state.job_description == "":
        st.warning("⚠ Please enter Job Description first.")
        st.stop()


    # Create interview history only once
    if "chat_history" not in st.session_state:

        st.session_state.chat_history = create_history(
            st.session_state.resume_text,
            st.session_state.job_description
        )


    # Start Interview
    if st.button("▶ Start Interview"):
        
        if st.session_state.interview_start_time is None:
           st.session_state.interview_start_time = time.time()

        reply = interview_chat(
            st.session_state.chat_history
        )

        st.session_state.chat_history.append(
            {
                "role": "assistant",
                "content": reply
            }
        )

        st.rerun()
        
        # Interview Timer

    if st.session_state.interview_start_time:

        elapsed = int(
            time.time() - st.session_state.interview_start_time
        )

        remaining = 900 - elapsed

        if remaining > 0:

            mins = remaining // 60
            secs = remaining % 60

            st.info(
                f"⏱ Interview Time Remaining: {mins:02d}:{secs:02d}"
            )

        else:
            st.error("⏰ Interview Time Completed")
            st.stop()
            
            
    # Show Chat
    for msg in st.session_state.chat_history:

        if msg["role"] == "assistant":
            st.chat_message("assistant").write(msg["content"])

        elif msg["role"] == "user":
            st.chat_message("user").write(msg["content"])


    # Candidate Answer
    user_input = st.chat_input("Type your answer...")

    if user_input:

        st.session_state.chat_history.append(
            {
                "role": "user",
                "content": user_input
            }
        )

        reply = interview_chat(
            st.session_state.chat_history
        )

        st.session_state.chat_history.append(
            {
                "role": "assistant",
                "content": reply
            }
        )

        st.rerun()


   # Count only user answers
    user_answers = [
        msg for msg in st.session_state.get("chat_history", [])
        if msg["role"] == "user"
    ]

    if "chat_history" in st.session_state and len(st.session_state.chat_history) > 2:

        st.divider()

        if st.button("✅ Finish Interview"):

            if len(user_answers) < 3:
                st.warning("⚠ Please answer at least 3 interview questions before finishing.")

            else:
                analysis = analyze_interview(
                    st.session_state.resume_text,
                    st.session_state.job_description,
                    st.session_state.chat_history
                )

                st.session_state.interview_analysis = analysis

                st.success("✅ Interview Evaluation Completed!")

        # ✅ Always show analysis
        if st.session_state.get("interview_analysis"):

            st.divider()
            st.subheader("📊 Interview Analysis")
            st.write(st.session_state.interview_analysis)



# -------------------------------
# COVER LETTER
# -------------------------------

elif page == "📝 Cover Letter":

    from modules.cover_letter import generate_cover_letter

    st.title("✉️ AI Cover Letter Generator")

    if st.session_state.resume_text == "":
        st.warning("Upload and analyze resume first")
        st.stop()

    elif st.session_state.job_description == "":
        st.warning("Add Job Description first")
        st.stop()

    else:

        st.subheader("Create Personalized Cover Letter")

        if st.button(
            "✨ Generate Cover Letter",
        
        ):

            with st.spinner(
                "AI is writing your personalized cover letter..."
            ):

                cover_letter = generate_cover_letter(
                    st.session_state.resume_text,
                    st.session_state.job_description
                )

                st.session_state.cover_letter = cover_letter

        if st.session_state.get("cover_letter"):

            st.divider()

            st.success(
                "Your personalized cover letter is ready!"
            )

            st.markdown(
               f"""
            <div class="cover-box">
            {st.session_state.cover_letter}
             </div>
               """,
           unsafe_allow_html=True
            )

            st.download_button(
                label="📥 Download Cover Letter",
                data=st.session_state.cover_letter,
                file_name="AI_Cover_Letter.txt",
                mime="text/plain"
            )
# -------------------------------
# ROADMAP
# -------------------------------
elif page == "📚 Learning Roadmap":

    from modules.learning_roadmap import generate_learning_roadmap

    st.title("📚 AI Learning Roadmap")

    if st.session_state.resume_text == "":
        st.warning("Please analyze your resume first.")
        st.stop()

    if st.session_state.job_description == "":
        st.warning("Please enter Job Description.")
        st.stop()

    if st.button("🚀 Generate Learning Roadmap"):

        with st.spinner("Generating Roadmap..."):

            roadmap = generate_learning_roadmap(
                st.session_state.resume_text,
                st.session_state.job_description
            )

            st.session_state.learning_roadmap = roadmap

    if st.session_state.get("learning_roadmap"):

        st.success("Roadmap Generated Successfully")

        st.markdown(st.session_state.learning_roadmap)

# -------------------------------
# REPORT
# -------------------------------

elif page == "📑 Final Report":

    from modules.report_generator import generate_report_data
    from modules.pdf_generator import create_pdf

    import os


    st.title("📑 Final Report")


    if st.session_state.resume_text == "":
        st.warning("⚠ Please analyze your resume first.")
        st.stop()


    if st.button("📄 Generate Final Report"):


        with st.spinner("Generating professional report..."):


            # Step 1: Collect all data
            report_data = generate_report_data(
                st.session_state
            )


            # Step 2: PDF location
            pdf_path = os.path.join(
    os.getcwd(),
    "AI_Career_Report.pdf"
)


            # Step 3: Create PDF
            create_pdf(
            report_data,
            pdf_path
            )

            st.success(
           "✅ Final Report Generated Successfully!"
            )


            # Save path
            st.session_state.report_pdf = pdf_path



    # Download Button

    if st.session_state.get("report_pdf"):

        with open(
            st.session_state.report_pdf,
            "rb"
        ) as pdf_file:


            st.download_button(
                label="📥 Download Career Report PDF",
                data=pdf_file,
                file_name="AI_Career_Assessment_Report.pdf",
                mime="application/pdf"
            )
            
            
import re

def extract_candidate_name(resume_text):

    lines = resume_text.split("\n")

    for line in lines:

        line = line.strip()

        # Skip empty lines
        if not line:
            continue

        # Skip common headings
        if any(word in line.lower() for word in [
            "resume",
            "curriculum",
            "b.tech",
            "computer science",
            "objective",
            "education",
            "email",
            "phone",
            "mobile"
        ]):
            continue

        # Candidate name usually has 2–4 words
        words = line.split()

        if 2 <= len(words) <= 4:
            return line

    return "Candidate"
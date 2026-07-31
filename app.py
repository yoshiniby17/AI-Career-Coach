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


# -------------------------------
# PAGE CONFIG (only ONCE)
# -------------------------------
st.set_page_config(
    page_title="AI Career Coach",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

import base64

def get_base64(file_path):
    with open(file_path, "rb") as f:
        return base64.b64encode(f.read()).decode()

bg = get_base64("assets/images/background.png")


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
# LOAD CSS
# -------------------------------
def load_css():
    with open("style.css") as f:
        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True
        )

load_css()

st.markdown(f"""
<style>

.stApp {{
    background-image:
        linear-gradient(
            rgba(8,15,35,0.20),
            rgba(8,15,35,0.30)
        ),
        url("data:image/png;base64,{bg}");

    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    background-attachment: fixed;
}}

</style>
""", unsafe_allow_html=True)
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
# SIDEBAR BACKGROUND STYLE
# -------------------------------

sidebar_bg = get_base64("assets/images/ai_background.png")

st.markdown(f"""
<style>

section[data-testid="stSidebar"] {{
    background-image:
        linear-gradient(
            rgba(8,15,35,0.55),
            rgba(8,15,35,0.55)
        ),
        url("data:image/png;base64,{sidebar_bg}") !important;

    background-size: cover !important;
    background-position: center !important;
    background-repeat: no-repeat !important;
}}

section[data-testid="stSidebar"] > div {{
    background: transparent !important;
}}

section[data-testid="stSidebar"] * {{
    color: white !important;
}}

</style>
""", unsafe_allow_html=True)

# -------------------------------
# SIDEBAR
# -------------------------------

# Logo (Optional)
# st.sidebar.image("assets/logo.png", width=120)

with st.sidebar:

    st.markdown("""
    <div style="text-align:center;padding:10px 0 20px 0;">
        <h2 style="color:white;margin-bottom:5px;">🤖 AI Career Coach</h2>
        <p style="color:#94A3B8;font-size:14px;">
            Smart Resume & Career Assistant
        </p>
        <hr style="border:1px solid #334155;">
    </div>
    """, unsafe_allow_html=True)

    page = st.radio(
        "",
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

    st.markdown("""
<div class="hero-banner">

<h1>🤖 AI Career Coach Pro</h1>

<h3>Analyze • Improve • Get Hired</h3>

<p style="font-size:18px;">
Your AI-powered career assistant for Resume Analysis, ATS Optimization,
Interview Preparation, Cover Letter Generation and Career Roadmap.
</p>

<p style="font-size:16px;opacity:0.9;">
✨ <b>"Success begins with preparation. Let AI guide your career."</b>
</p>

</div>
""", unsafe_allow_html=True)

    # Dashboard Status
    resume_uploaded = bool(st.session_state.get("resume_text"))
    ats = st.session_state.get("ats_score", None)
    jd_match = st.session_state.get("jd_match_score", None)
    interview_done = bool(st.session_state.get("interview_analysis"))
    report_ready = bool(st.session_state.get("report_pdf"))

    # ---------------- Metric Cards ----------------

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-icon">📄</div>
            <div class="metric-title">Resume</div>
            <div class="metric-value">
                {"Uploaded" if resume_uploaded else "Not Uploaded"}
            </div>
            <div class="metric-sub">Upload your resume</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:

        ats_text = "--"

        if ats:
            ats_text = f"{ats['score']}%"

        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-icon">🎯</div>
            <div class="metric-title">ATS Score</div>
            <div class="metric-value">{ats_text}</div>
            <div class="metric-sub">Resume Analysis</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:

        jd_text = "--"

        if jd_match is not None:
            jd_text = f"{jd_match}%"

        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-icon">💼</div>
            <div class="metric-title">JD Match</div>
            <div class="metric-value">{jd_text}</div>
            <div class="metric-sub">Job Compatibility</div>
        </div>
        """, unsafe_allow_html=True)

    with col4:

        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-icon">🤖</div>
            <div class="metric-title">AI Status</div>
            <div class="metric-value">
                {"Ready" if resume_uploaded else "Waiting"}
            </div>
            <div class="metric-sub">Career Assistant</div>
        </div>
        """, unsafe_allow_html=True)

    st.write("")

    # ---------------- Quick Actions & Progress ----------------

    left, right = st.columns(2)

    with left:

        st.markdown("### 🚀 Quick Actions")

        st.info("📄 Upload Resume")
        st.info("💼 Paste Job Description")
        st.info("🤖 Analyze Resume")
        st.info("🎯 Check ATS Score")
        st.info("🎤 Start AI Interview")
        st.info("📑 Download Final Report")

    with right:

        st.markdown("### 📈 Progress")

        st.success("✅ Resume Uploaded" if resume_uploaded else "⬜ Resume Not Uploaded")
        st.success("✅ ATS Completed" if ats else "⬜ ATS Pending")
        st.success("✅ JD Matching Completed" if jd_match is not None else "⬜ JD Matching Pending")
        st.success("✅ Interview Completed" if interview_done else "⬜ Interview Pending")
        st.success("✅ Report Generated" if report_ready else "⬜ Report Pending")

    st.write("")

    # ---------------- Recent Activity ----------------

    st.markdown("### 🔥 Recent Activity")

    if resume_uploaded:
        st.success("📄 Resume uploaded successfully.")

    if ats:
        st.success("🎯 ATS Score generated.")

    if jd_match is not None:
        st.success("💼 JD Matching completed.")

    if interview_done:
        st.success("🎤 Interview completed.")

    if report_ready:
        st.success("📑 Final Report generated.")

    if not any([
        resume_uploaded,
        ats,
        jd_match is not None,
        interview_done,
        report_ready
    ]):
        st.info("No activity yet. Upload your resume to get started.")
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


    if "resume_file" not in st.session_state:
        st.session_state.resume_file = None

    if "resume_name" not in st.session_state:
        st.session_state.resume_name = ""


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
        key="jd_input"
    )


    st.session_state.job_description = job_description



    if st.button("Analyze Resume"):


        if resume is None:

            st.warning("Please upload resume.")


        elif job_description.strip() == "":

            st.warning("Please paste Job Description.")


        else:

            resume_text = extract_resume(resume)

            st.session_state.resume_text = resume_text


            st.session_state.candidate_name = extract_candidate_name(
                resume_text
            )


            with st.spinner("🤖 AI is analyzing your resume..."):

                time.sleep(1)

                analysis = analyze_resume(
                resume_text,
                job_description
                )

                time.sleep(0.5)

                ats = calculate_ats_score(
                resume_text,
                job_description
                )

                time.sleep(0.5)

                match_score = calculate_jd_match(
                resume_text,
                job_description
                )

            st.session_state.resume_analysis = analysis
            st.session_state.ats_score = ats
            st.session_state.jd_match_score = match_score


            st.toast("🎉 Resume Analysis Completed", icon="🎉")

            st.markdown("""
            <div style="
            padding:15px;
            background:#16A34A;
            color:white;
            border-radius:10px;
            font-weight:bold;
            text-align:center;
            margin-top:10px;
            ">
            ✅ AI Analysis Completed Successfully
            </div>
            """, unsafe_allow_html=True)

    # Always show Resume Analysis

    if st.session_state.get("resume_analysis"):

        st.divider()

        st.subheader("📄 Resume Analysis")

        st.write(
            st.session_state.resume_analysis
        )
        
        
        
# -------------------------------
# ATS SCORE
# -------------------------------

elif page == "📊 ATS Score":

    st.title("📊 ATS Score")

    ats = st.session_state.get("ats_score", None)

    if ats is None:
        st.warning("⚠ Please analyze your resume first.")

    else:

        # If ATS is stored as integer
        if isinstance(ats, int):

            ats = {
                "score": ats,
                "matched": [],
                "missing": []
            }

        # Metrics
        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "ATS Score",
                f"{ats['score']}%"
            )

            st.progress(ats["score"] / 100)


        with col2:

            st.metric(
                "Matched Skills",
                len(ats.get("matched", []))
            )


        with col3:

            st.metric(
                "Missing Skills",
                len(ats.get("missing", []))
            )


        st.divider()


        # Skills Lists

        col1, col2 = st.columns(2)


        with col1:

            st.success("✅ Matched Skills")

            matched = ats.get("matched", [])

            if matched:

                for skill in matched:
                    st.write(f"✔ {skill}")

            else:

                st.info("No matched skills found.")



        with col2:

            st.error("❌ Missing Skills")

            missing = ats.get("missing", [])

            if missing:

                for skill in missing:
                    st.write(f"⚠ {skill}")

            else:

                st.success("No missing skills.")

# -------------------------------
# JD MATCH
# -------------------------------

elif page == "🎯 JD Matching":

    st.title("🎯 JD Matching")

    if "jd_match_score" not in st.session_state:
        st.warning("⚠ Please analyze your resume first.")

    else:
    

           st.subheader("📊 JD Match Score")

           jd = st.session_state.jd_match_score

           st.metric(
           "JD Match Score",
           f"{jd}%"
           )

           st.progress(jd / 100)

           st.success(
           f"Your resume matches {jd}% with the Job Description."
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

              with st.spinner("🤖 AI is evaluating your interview..."):

                 analysis = analyze_interview(
                     st.session_state.resume_text,
                     st.session_state.job_description,
                     st.session_state.chat_history
                 )

                 st.session_state.interview_analysis = analysis

                 
        # Show interview analysis ONLY here
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

    st.divider()

    st.caption(
    "Built with ❤️ using Python • Streamlit • Groq"
)
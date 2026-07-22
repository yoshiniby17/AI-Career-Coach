from datetime import datetime
import uuid


def generate_report_data(session_state):

    report = {

        "candidate_name": session_state.get(
            "candidate_name",
            "Candidate"
        ),

        "report_id": f"ACCR-{datetime.now().strftime('%Y%m%d')}-{str(uuid.uuid4())[:4].upper()}",

        "generated_date": datetime.now().strftime("%d %B %Y"),

        "resume_analysis": session_state.get(
            "resume_analysis",
            "Not Available"
        ),

        "ats_result": session_state.get(
              "ats_score",
               {}
        ),

        "interview_analysis": session_state.get(
            "interview_analysis",
            "Not Available"
        ),

        "cover_letter": session_state.get(
            "cover_letter",
            "Not Available"
        ),

        "learning_roadmap": session_state.get(
            "learning_roadmap",
            "Not Available"
        )

    }

    return report
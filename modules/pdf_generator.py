from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    PageBreak
)

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.units import inch


def create_pdf(report_data, file_path):

    doc = SimpleDocTemplate(
        file_path,
        pagesize=(8.5*inch, 11*inch),
        rightMargin=50,
        leftMargin=50,
        topMargin=50,
        bottomMargin=50
    )


    styles = getSampleStyleSheet()


    title_style = styles["Title"]

    title_style.fontSize = 24
    title_style.alignment = TA_CENTER


    heading_style = styles["Heading2"]

    heading_style.fontSize = 18


    body_style = styles["BodyText"]

    body_style.fontSize = 11
    body_style.leading = 16


    content = []
    
    
    # -----------------------------
    # RESUME ANALYSIS
    # -----------------------------

    content.append(
        Paragraph(
            "Resume Analysis",
            heading_style
        )
    )

    content.append(
        Spacer(1, 10)
    )


    resume_analysis = report_data.get(
        "resume_analysis",
        "Not Available"
    )


    content.append(
        Paragraph(
            str(resume_analysis).replace("\n", "<br/>"),
            body_style
        )
    )


    content.append(
        Spacer(1, 20)
    )


    # -----------------------------
    # ATS ANALYSIS
    # -----------------------------

    content.append(
    Paragraph(
        "ATS Analysis",
        heading_style
    )
)

    content.append(
    Spacer(1, 10)
)

    ats_result = report_data.get("ats_result", {})

    if isinstance(ats_result, dict):

      ats_text = f"""
      <b>ATS Score:</b> {ats_result.get("score", 0)}%<br/><br/>

       <b>Matched Skills:</b><br/>
    {", ".join(ats_result.get("matched", []))}<br/><br/>

    <b>Missing Skills:</b><br/>
    {", ".join(ats_result.get("missing", []))}
    """

    else:

        ats_text = "Not Available"

    content.append(
        Paragraph(
            ats_text,
            body_style
        )
    )

    content.append(
        PageBreak()
    )
        
            # -----------------------------
        # INTERVIEW ANALYSIS
        # -----------------------------

    content.append(
            Paragraph(
                "Interview Analysis",
                heading_style
            )
        )

    content.append(
            Spacer(1, 10)
        )


    interview_analysis = report_data.get(
            "interview_analysis",
            "Not Available"
        )


    content.append(
            Paragraph(
                str(interview_analysis).replace("\n", "<br/>"),
                body_style
            )
        )


    content.append(
            Spacer(1, 20)
        )


        # -----------------------------
        # COVER LETTER
        # -----------------------------

    content.append(
            Paragraph(
                "Cover Letter",
                heading_style
            )
        )


    content.append(
            Spacer(1, 10)
        )


    cover_letter = report_data.get(
            "cover_letter",
            "Not Available"
        )


    content.append(
            Paragraph(
                str(cover_letter).replace("\n", "<br/>"),
                body_style
            )
        )


    content.append(
            PageBreak()
        )
        
    # -----------------------------
    # BUILD PDF
    # -----------------------------

    doc.build(content)
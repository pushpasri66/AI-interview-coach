import os
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle


class ATSService:
    """Service generating downloadable PDF analysis reports in reports/interview_reports/."""

    def generate_pdf_report(self, user_name: str, resume_obj, analysis_obj) -> str:
        """Generates PDF report and saves it to reports/interview_reports/."""
        reports_dir = os.path.join(os.path.dirname(__file__), "..", "..", "reports", "interview_reports")
        os.makedirs(reports_dir, exist_ok=True)

        filename = f"resume_report_{resume_obj.user_id}_{resume_obj.id}.pdf"
        filepath = os.path.join(reports_dir, filename)

        doc = SimpleDocTemplate(
            filepath,
            pagesize=letter,
            rightMargin=36,
            leftMargin=36,
            topMargin=36,
            bottomMargin=36
        )

        styles = getSampleStyleSheet()

        # Custom Paragraph Styles
        title_style = ParagraphStyle(
            "DocTitle",
            parent=styles["Title"],
            fontName="Helvetica-Bold",
            fontSize=22,
            leading=26,
            textColor=colors.HexColor("#0f172a"),
            alignment=0
        )

        h2_style = ParagraphStyle(
            "SectionH2",
            parent=styles["Heading2"],
            fontName="Helvetica-Bold",
            fontSize=14,
            leading=18,
            textColor=colors.HexColor("#6366f1"),
            spaceBefore=12,
            spaceAfter=6
        )

        body_style = ParagraphStyle(
            "BodyTextCustom",
            parent=styles["BodyText"],
            fontName="Helvetica",
            fontSize=10,
            leading=14,
            textColor=colors.HexColor("#334155")
        )

        bullet_style = ParagraphStyle(
            "BulletCustom",
            parent=styles["BodyText"],
            fontName="Helvetica",
            fontSize=9.5,
            leading=13,
            textColor=colors.HexColor("#1e293b"),
            leftIndent=15,
            spaceAfter=4
        )

        story = []

        # 1. Header Title
        story.append(Paragraph("AI Interview Coach - Resume Analysis Report", title_style))
        story.append(Spacer(1, 4))
        story.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor("#6366f1"), spaceAfter=15))

        # 2. Metadata Table
        upload_date_str = resume_obj.upload_date.strftime("%B %d, %Y %H:%M") if resume_obj.upload_date else "N/A"
        parsed_data = analysis_obj.get_parsed_data()

        meta_data = [
            [Paragraph(f"<b>Candidate Name:</b> {user_name}", body_style), Paragraph(f"<b>Upload Date:</b> {upload_date_str}", body_style)],
            [Paragraph(f"<b>File Name:</b> {resume_obj.original_filename}", body_style), Paragraph(f"<b>ATS Score:</b> <font color='{analysis_obj.get_recommendations().get('color', '#6366f1')}'><b>{analysis_obj.ats_score} / 100</b></font>", body_style)]
        ]

        meta_table = Table(meta_data, colWidths=[270, 270])
        meta_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#f8fafc")),
            ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#e2e8f0")),
            ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
            ('PADDING', (0,0), (-1,-1), 8),
        ]))
        story.append(meta_table)
        story.append(Spacer(1, 15))

        # 3. Strengths Section
        story.append(Paragraph("Key Resume Strengths", h2_style))
        strengths = analysis_obj.get_strengths()
        for s in strengths:
            story.append(Paragraph(f"• {s}", bullet_style))
        story.append(Spacer(1, 10))

        # 4. Weaknesses Section
        story.append(Paragraph("Areas for Improvement (Weaknesses)", h2_style))
        weaknesses = analysis_obj.get_weaknesses()
        for w in weaknesses:
            story.append(Paragraph(f"• {w}", bullet_style))
        story.append(Spacer(1, 10))

        # 5. Suggestions Section
        story.append(Paragraph("Actionable Suggestions", h2_style))
        suggestions = analysis_obj.get_suggestions()
        for sg in suggestions:
            story.append(Paragraph(f"• {sg}", bullet_style))
        story.append(Spacer(1, 10))

        # 6. Technical Skills Detected
        story.append(Paragraph("Extracted Technical Skills", h2_style))
        tech_skills = parsed_data.get("technical_skills", [])
        skills_str = ", ".join(tech_skills) if tech_skills else "None explicitly extracted"
        story.append(Paragraph(f"<b>Identified Skills:</b> {skills_str}", body_style))
        story.append(Spacer(1, 10))

        # 7. AI Course Recommendations
        story.append(Paragraph("Recommended Courses & Next Steps", h2_style))
        recs = analysis_obj.get_recommendations()
        courses = recs.get("recommended_courses", [])
        for c in courses:
            story.append(Paragraph(f"• <b>{c.get('title')}</b> - {c.get('provider')} ({c.get('level')})", bullet_style))

        # Build PDF Document
        doc.build(story)

        # Return relative report path for DB storage
        rel_path = f"reports/interview_reports/{filename}"
        return rel_path

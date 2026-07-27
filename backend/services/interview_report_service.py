import os
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle


class InterviewReportService:
    """Service generating downloadable PDF performance reports for interview sessions."""

    def generate_pdf_report(self, user_name: str, interview_obj, questions: list, answers_dict: dict) -> str:
        """Generates PDF interview report and saves it to reports/interview_reports/."""
        reports_dir = os.path.join(os.path.dirname(__file__), "..", "..", "reports", "interview_reports")
        os.makedirs(reports_dir, exist_ok=True)

        filename = f"interview_report_{interview_obj.user_id}_{interview_obj.id}.pdf"
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
            fontSize=13,
            leading=17,
            textColor=colors.HexColor("#6366f1"),
            spaceBefore=10,
            spaceAfter=4
        )

        body_style = ParagraphStyle(
            "BodyTextCustom",
            parent=styles["BodyText"],
            fontName="Helvetica",
            fontSize=9.5,
            leading=13.5,
            textColor=colors.HexColor("#334155")
        )

        story = []

        # Title
        story.append(Paragraph(f"AI Interview Coach - {interview_obj.interview_type.upper()} Interview Report", title_style))
        story.append(Spacer(1, 4))
        story.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor("#6366f1"), spaceAfter=12))

        # Metadata Table
        completed_str = interview_obj.completed_at.strftime("%B %d, %Y %H:%M") if interview_obj.completed_at else datetime.utcnow().strftime("%B %d, %Y")
        comp_info = f" ({interview_obj.company_name})" if interview_obj.company_name else ""
        
        meta_data = [
            [Paragraph(f"<b>Candidate:</b> {user_name}", body_style), Paragraph(f"<b>Date:</b> {completed_str}", body_style)],
            [Paragraph(f"<b>Type:</b> {interview_obj.interview_type.title()}{comp_info}", body_style), Paragraph(f"<b>Overall Score:</b> <font color='#6366f1'><b>{interview_obj.score} / 100</b></font>", body_style)],
            [Paragraph(f"<b>Difficulty:</b> {interview_obj.difficulty.title()}", body_style), Paragraph(f"<b>Questions Completed:</b> {len(answers_dict)} / {len(questions)}", body_style)]
        ]

        meta_table = Table(meta_data, colWidths=[270, 270])
        meta_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#f8fafc")),
            ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#e2e8f0")),
            ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
            ('PADDING', (0,0), (-1,-1), 6),
        ]))
        story.append(meta_table)
        story.append(Spacer(1, 12))

        # Questions Breakdown
        story.append(Paragraph("Question-by-Question Evaluation", h2_style))

        for idx, q in enumerate(questions, 1):
            ans = answers_dict.get(q.id)
            score = ans.answer_score if ans else 0
            user_ans_text = ans.user_answer if ans else "No response provided."
            feedback = ans.feedback if ans else "N/A"

            q_title = f"<b>Q{idx}. [{q.category or 'General'}] {q.question_text}</b>"
            story.append(Paragraph(q_title, body_style))
            
            ans_info = f"<b>Your Answer:</b> {user_ans_text}<br/><b>Score:</b> {score}/100 | <b>Feedback:</b> {feedback}"
            story.append(Paragraph(ans_info, ParagraphStyle("Ans", parent=body_style, leftIndent=12, spaceAfter=8)))

        doc.build(story)

        rel_path = f"reports/interview_reports/{filename}"
        return rel_path

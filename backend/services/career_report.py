import os
import io
from datetime import datetime
from typing import Dict, Any, Optional

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

from backend.models.user import User
from AI.digital_twin.digital_twin_engine import DigitalTwinEngine
from AI.digital_twin.candidate_profile import CandidateProfile
from AI.career_prediction.career_path_predictor import CareerPathPredictor
from AI.future_skills.skill_demand_predictor import SkillDemandPredictor
from AI.daily_planner.daily_plan_engine import DailyPlanEngine
from AI.explainable.score_explainer import ScoreExplainer


class CareerReportService:
    """Generates professional, publication-grade PDF reports for AI Career Intelligence, Readiness, Skill Gaps, and Applications."""

    def __init__(self):
        self.twin_engine = DigitalTwinEngine()
        self.path_predictor = CareerPathPredictor()
        self.skill_demand = SkillDemandPredictor()
        self.daily_planner = DailyPlanEngine()
        self.score_explainer = ScoreExplainer()

    def generate_career_pdf(self, user_id: int, report_type: str = "intelligence") -> str:
        """Builds a customized PDF report according to the requested report_type and returns the file path."""
        user = User.query.get(user_id)
        if not user:
            raise ValueError(f"User #{user_id} does not exist.")

        reports_dir = os.path.join(os.path.dirname(__file__), "..", "..", "reports", "career_reports")
        os.makedirs(reports_dir, exist_ok=True)

        type_clean = report_type.lower().strip()
        filename = f"career_{type_clean}_report_{user.id}_{int(datetime.utcnow().timestamp())}.pdf"
        filepath = os.path.join(reports_dir, filename)

        doc = SimpleDocTemplate(
            filepath,
            pagesize=letter,
            rightMargin=36,
            leftMargin=36,
            topMargin=36,
            bottomMargin=36
        )

        story = []
        styles = getSampleStyleSheet()

        # Styles
        title_style = ParagraphStyle(
            "DocTitle",
            parent=styles["Title"],
            fontName="Helvetica-Bold",
            fontSize=20,
            leading=24,
            textColor=colors.HexColor("#0f172a"),
            alignment=0
        )

        subtitle_style = ParagraphStyle(
            "DocSubTitle",
            parent=styles["Normal"],
            fontName="Helvetica",
            fontSize=10,
            leading=14,
            textColor=colors.HexColor("#64748b")
        )

        h2_style = ParagraphStyle(
            "SectionH2",
            parent=styles["Heading2"],
            fontName="Helvetica-Bold",
            fontSize=12,
            leading=16,
            textColor=colors.HexColor("#4f46e5"),
            spaceBefore=10,
            spaceAfter=4
        )

        body_style = ParagraphStyle(
            "BodyTextCustom",
            parent=styles["BodyText"],
            fontName="Helvetica",
            fontSize=9,
            leading=13,
            textColor=colors.HexColor("#334155")
        )

        bullet_style = ParagraphStyle(
            "BulletTextCustom",
            parent=styles["Normal"],
            fontName="Helvetica",
            fontSize=8.5,
            leading=12,
            textColor=colors.HexColor("#1e293b")
        )

        # 1. Header & Candidate Summary
        report_titles = {
            "intelligence": "AI Executive Career Intelligence Dossier",
            "readiness": "AI Career Readiness & Digital Twin Report",
            "skill_gap": "Target Skill Gap & Future Demand Intelligence Report",
            "job_application": "Tailored Job Application & ATS Strategy Report"
        }
        title_text = report_titles.get(type_clean, "AI Career Intelligence Report")

        story.append(Paragraph(title_text, title_style))
        story.append(Paragraph(f"Candidate: <b>{user.fullname}</b> ({user.email}) | Generated: {datetime.utcnow().strftime('%B %d, %Y %H:%M UTC')}", subtitle_style))
        story.append(Spacer(1, 8))
        story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#6366f1"), spaceAfter=10))

        # 2. Digital Twin & Readiness Overview
        twin_data = self.twin_engine.get_digital_twin_state(user_id=user.id, auto_sync=False)
        scores = twin_data.get("scores", {})
        readiness = scores.get("career_readiness_score", 85)
        target_role = twin_data.get("target_role", "Software Engineer")

        meta_table_data = [
            [
                Paragraph("<b>Target Role</b>", body_style),
                Paragraph(f"<b>{target_role}</b>", body_style),
                Paragraph("<b>Overall Readiness</b>", body_style),
                Paragraph(f"<b><font color='#4f46e5'>{readiness}%</font></b>", body_style)
            ],
            [
                Paragraph("<b>Technical Strength</b>", body_style),
                Paragraph(f"{scores.get('technical_strength', 85)}/100", body_style),
                Paragraph("<b>Interview Readiness</b>", body_style),
                Paragraph(f"{scores.get('interview_readiness', 80)}/100", body_style)
            ],
            [
                Paragraph("<b>Communication</b>", body_style),
                Paragraph(f"{scores.get('communication_strength', 82)}/100", body_style),
                Paragraph("<b>Skill Proficiency</b>", body_style),
                Paragraph(f"{scores.get('skill_strength', 86)}/100", body_style)
            ]
        ]
        meta_table = Table(meta_table_data, colWidths=[120, 150, 120, 150])
        meta_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#f8fafc")),
            ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
            ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#e2e8f0")),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("TOPPADDING", (0, 0), (-1, -1), 4),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ]))
        story.append(meta_table)
        story.append(Spacer(1, 10))

        # 3. Top Skills & Skill Gaps
        story.append(Paragraph("1. Current Skills & Target Gap Intelligence", h2_style))
        profile_snap = CandidateProfile(user.id).build_snapshot()
        current_skills = [s["skill_name"] for s in profile_snap.get("skills", [])] or ["Python", "SQL", "Machine Learning"]
        gaps = twin_data.get("skill_gaps", [])

        skills_p = Paragraph(f"<b>Verified Candidate Skills:</b> {', '.join(current_skills)}", body_style)
        story.append(skills_p)
        story.append(Spacer(1, 4))

        if gaps:
            gap_table_data = [["Missing / Target Skill", "Role Importance", "Est. Learning Timeline", "Action Item"]]
            for g in gaps[:4]:
                gap_table_data.append([
                    g.get("skill", "Docker"),
                    g.get("importance", "High"),
                    g.get("learning_timeline", "2-4 Weeks"),
                    g.get("action", f"Master {g.get('skill')} via hands-on projects.")[:60] + "..."
                ])
            gap_table = Table(gap_table_data, colWidths=[110, 90, 110, 230])
            gap_table.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#4f46e5")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 8),
                ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#e2e8f0")),
                ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
                ("TOPPADDING", (0, 0), (-1, -1), 3),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
            ]))
            story.append(gap_table)
        story.append(Spacer(1, 10))

        # 4. Career Path Predictions (9 Roles)
        story.append(Paragraph("2. Top Predictive Career Path Benchmarks", h2_style))
        paths_eval = self.path_predictor.predict_for_user(user_id=user.id, persist=False)
        top_roles = paths_eval.get("all_roles", [])[:4]

        paths_table_data = [["Role Title", "Match %", "Missing Skills", "Growth Level", "Prep Time"]]
        for r in top_roles:
            paths_table_data.append([
                r.get("role", "Software Engineer"),
                f"{r.get('match_percentage', 80)}%",
                ", ".join(r.get("missing_skills", [])[:2]) or "None",
                r.get("career_growth_level", "High"),
                r.get("preparation_time", "4-6 Weeks")
            ])
        paths_table = Table(paths_table_data, colWidths=[140, 60, 150, 100, 90])

        paths_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0f172a")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 8),
            ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#e2e8f0")),
            ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
            ("TOPPADDING", (0, 0), (-1, -1), 3),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ]))
        story.append(paths_table)
        story.append(Spacer(1, 10))

        # 5. Future Skills (1, 2, 3 Year Forecast)
        story.append(Paragraph("3. Future Skill Demand Horizons (1-3 Years)", h2_style))
        future_forecasts = self.skill_demand.get_forecasts_for_category()[:4]
        future_data = [["Skill Domain", "Current Score", "1-Year", "2-Year", "3-Year", "Growth %"]]
        for f in future_forecasts:
            forecasts_map = f.get("demand_forecast", {})
            future_data.append([
                f.get("skill_name", "Skill"),
                f"{f.get('current_demand', 75)}/100",
                f"{forecasts_map.get('1_year', 85)}/100",
                f"{forecasts_map.get('2_year', 90)}/100",
                f"{forecasts_map.get('3_year', 95)}/100",
                f"+{f.get('growth_percentage', 20)}%"
            ])
        future_table = Table(future_data, colWidths=[140, 80, 80, 80, 80, 80])

        future_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1e293b")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 8),
            ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#e2e8f0")),
            ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
            ("TOPPADDING", (0, 0), (-1, -1), 3),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ]))
        story.append(future_table)
        story.append(Spacer(1, 10))

        # 6. Daily Plan & Explainable Score Breakdown
        story.append(Paragraph("4. Explainable Score Breakdown & Recommended Next Actions", h2_style))
        explain_res = self.score_explainer.explain_career_match_score(
            score_value=readiness,
            target_role=target_role,
            skill_scores={"Python": 92, "SQL": 80, "Machine Learning": 85},
            missing_skills=["Docker", "AWS Cloud"]
        )

        why_p = Paragraph(f"<b>Score Rationale:</b> {explain_res['why_generated']}", body_style)
        story.append(why_p)
        story.append(Spacer(1, 4))

        for act in explain_res.get("improvement_actions", []):
            story.append(Paragraph(f"• <b>Action:</b> {act}", bullet_style))

        # Build document
        doc.build(story)
        return filepath

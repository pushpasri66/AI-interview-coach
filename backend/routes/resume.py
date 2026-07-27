import os
import time
from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app, send_file
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename

from backend.database import db
from backend.models.resume import Resume, ResumeAnalysis
from backend.services.resume_parser import ResumeParser
from backend.services.ats_service import ATSService
from backend.services.analytics_service import AnalyticsService

from AI.models.ats_score import ATSScoreCalculator
from AI.models.resume_analysis import ResumeAnalyzer
from AI.models.recommendation import ResumeRecommender

resume_bp = Blueprint("resume", __name__, url_prefix="/resume")

ALLOWED_EXTENSIONS = {"pdf", "docx"}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB limit


def allowed_file(filename: str) -> bool:
    """Validates file extension."""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@resume_bp.route("/upload", methods=["GET", "POST"])
@login_required
def upload():
    """Handles resume upload, parsing, ATS scoring, and report generation."""
    if request.method == "POST":
        if "resume_file" not in request.files:
            flash("No file part in upload request.", "danger")
            return redirect(request.url)

        file = request.files["resume_file"]

        if file.filename == "":
            flash("No file selected for upload.", "warning")
            return redirect(request.url)

        if not allowed_file(file.filename):
            flash("Invalid file format. Only PDF and DOCX files are allowed.", "danger")
            return redirect(request.url)

        # Check File Size
        file.seek(0, os.SEEK_END)
        file_length = file.tell()
        file.seek(0)

        if file_length > MAX_FILE_SIZE:
            flash("File size exceeds 5 MB limit. Please upload a smaller resume.", "danger")
            return redirect(request.url)

        try:
            # Secure original filename and generate userID_timestamp_filename format
            orig_filename = secure_filename(file.filename)
            ext = orig_filename.rsplit(".", 1)[1].lower()
            timestamp = int(time.time())
            unique_filename = f"{current_user.id}_{timestamp}_{orig_filename}"

            # Save file to uploads/resumes/
            upload_dir = os.path.join(current_app.root_path, "..", "uploads", "resumes")
            os.makedirs(upload_dir, exist_ok=True)
            saved_path = os.path.join(upload_dir, unique_filename)
            file.save(saved_path)

            current_app.logger.info(f"Resume uploaded by User #{current_user.id}: {unique_filename}")

            # 1. Parse Resume Text & Extract Fields
            parser = ResumeParser()
            raw_text = parser.extract_raw_text(saved_path)
            parsed_data = parser.parse_resume(raw_text)
            current_app.logger.info(f"Resume parsed for User #{current_user.id}. Word count: {parsed_data.get('word_count')}")

            # 2. Compute ATS Score
            ats_calc = ATSScoreCalculator()
            ats_results = ats_calc.compute_score(parsed_data, raw_text)
            current_app.logger.info(f"ATS Score generated for User #{current_user.id}: {ats_results.get('overall_score')}")

            # 3. Analyze Feedback (Strengths, Weaknesses, Suggestions)
            analyzer = ResumeAnalyzer()
            feedback = analyzer.analyze(parsed_data, ats_results)

            # 4. Generate AI Recommendations
            recommender = ResumeRecommender()
            recommendations = recommender.generate_recommendations(parsed_data)

            # Save Resume database record
            new_resume = Resume(
                user_id=current_user.id,
                filename=unique_filename,
                original_filename=orig_filename,
                file_path=saved_path,
                file_size=file_length,
                file_type=ext,
                is_active=True
            )
            db.session.add(new_resume)
            db.session.commit()

            # Save ResumeAnalysis database record
            analysis = ResumeAnalysis(
                resume_id=new_resume.id,
                user_id=current_user.id,
                ats_score=ats_results["overall_score"],
                extracted_text=raw_text
            )
            analysis.set_parsed_data(parsed_data)
            analysis.set_strengths(feedback["strengths"])
            analysis.set_weaknesses(feedback["weaknesses"])
            analysis.set_suggestions(feedback["suggestions"])

            # Attach ATS category & recommendation metadata to JSON
            combined_recs = {
                "color": ats_results["color"],
                "grade": ats_results["grade"],
                "explanation": ats_results["explanation"],
                "categories": ats_results["categories"],
                "missing_skills": recommendations["missing_skills"],
                "trending_technologies": recommendations["trending_technologies"],
                "recommended_courses": recommendations["recommended_courses"],
                "interview_prep_topics": recommendations["interview_prep_topics"],
                "resume_improvements": recommendations["resume_improvements"]
            }
            analysis.set_recommendations(combined_recs)

            db.session.add(analysis)
            db.session.commit()

            # 5. Generate PDF Report via ATSService
            ats_service = ATSService()
            report_rel_path = ats_service.generate_pdf_report(current_user.fullname, new_resume, analysis)
            analysis.report_path = report_rel_path
            db.session.commit()

            current_app.logger.info(f"PDF Report generated: {report_rel_path}")

            flash("Resume analyzed successfully!", "success")
            return redirect(url_for("resume.analysis", resume_id=new_resume.id))

        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Error processing resume upload for User #{current_user.id}: {str(e)}")
            flash(f"Error analyzing resume: {str(e)}", "danger")
            return redirect(request.url)

    return render_template("resume_upload.html")


@resume_bp.route("/analysis/<int:resume_id>")
@login_required
def analysis(resume_id: int):
    """Renders resume analysis dashboard with ATS scores and feedback."""
    resume_obj = Resume.query.filter_by(id=resume_id, user_id=current_user.id, is_active=True).first_or_404()
    analysis_obj = ResumeAnalysis.query.filter_by(resume_id=resume_obj.id).first_or_404()

    return render_template(
        "progress.html",
        resume=resume_obj,
        analysis=analysis_obj,
        parsed=analysis_obj.get_parsed_data(),
        strengths=analysis_obj.get_strengths(),
        weaknesses=analysis_obj.get_weaknesses(),
        suggestions=analysis_obj.get_suggestions(),
        recommendations=analysis_obj.get_recommendations()
    )


@resume_bp.route("/progress")
@login_required
def progress_latest():
    """Redirects to latest resume analysis or upload page if none exists."""
    latest_resume = Resume.query.filter_by(user_id=current_user.id, is_active=True).order_by(Resume.upload_date.desc()).first()
    if latest_resume:
        return redirect(url_for("resume.analysis", resume_id=latest_resume.id))
    flash("Please upload a resume first to view your ATS analysis.", "info")
    return redirect(url_for("resume.upload"))


@resume_bp.route("/history")
@login_required
def history():
    """Displays user's historical resumes and ATS score comparisons."""
    analytics_svc = AnalyticsService()
    comparison_data = analytics_svc.compare_resume_versions(current_user.id)

    return render_template(
        "resume_history.html",
        data=comparison_data
    )


@resume_bp.route("/download_report/<int:resume_id>")
@login_required
def download_report(resume_id: int):
    """Downloads the generated PDF report for a resume."""
    analysis_obj = ResumeAnalysis.query.filter_by(resume_id=resume_id, user_id=current_user.id).first_or_404()

    if not analysis_obj.report_path:
        flash("PDF report not available for this analysis.", "warning")
        return redirect(url_for("resume.analysis", resume_id=resume_id))

    abs_report_path = os.path.abspath(os.path.join(current_app.root_path, "..", analysis_obj.report_path))

    if not os.path.exists(abs_report_path):
        flash("PDF report file was not found on server.", "danger")
        return redirect(url_for("resume.analysis", resume_id=resume_id))

    return send_file(abs_report_path, as_attachment=True, download_name=f"ATS_Report_Resume_{resume_id}.pdf")


@resume_bp.route("/delete/<int:resume_id>", methods=["POST"])
@login_required
def delete_resume(resume_id: int):
    """Deletes a resume, associated analysis, PDF report, and physical file."""
    resume_obj = Resume.query.filter_by(id=resume_id, user_id=current_user.id).first_or_404()

    try:
        # Delete resume file from uploads/resumes/
        if os.path.exists(resume_obj.file_path):
            os.remove(resume_obj.file_path)

        # Delete PDF report if exists
        analysis_obj = ResumeAnalysis.query.filter_by(resume_id=resume_obj.id).first()
        if analysis_obj and analysis_obj.report_path:
            abs_report_path = os.path.abspath(os.path.join(current_app.root_path, "..", analysis_obj.report_path))
            if os.path.exists(abs_report_path):
                os.remove(abs_report_path)

        db.session.delete(resume_obj)
        db.session.commit()

        current_app.logger.info(f"Resume #{resume_id} deleted by User #{current_user.id}.")
        flash("Resume version deleted successfully.", "success")

    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error deleting resume #{resume_id}: {str(e)}")
        flash("An error occurred while deleting the resume.", "danger")

    return redirect(url_for("resume.history"))

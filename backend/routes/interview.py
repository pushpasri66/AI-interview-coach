import os
from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, current_app, send_file
from flask_login import login_required, current_user

from backend.database import db
from backend.models.interview import Interview, Question, Answer
from backend.models.resume import Resume, ResumeAnalysis
from backend.services.speech_service import SpeechService
from backend.services.coding_service import CodingService
from backend.services.interview_report_service import InterviewReportService

from AI.models.question_generator import QuestionGenerator
from AI.models.answer_evaluator import AnswerEvaluator

interview_bp = Blueprint("interview", __name__, url_prefix="/interview")


@interview_bp.route("/select")
@login_required
def select():
    """Renders main interview mode selection hub."""
    return render_template("interview_selection.html")


@interview_bp.route("/hr")
@login_required
def hr():
    """Renders HR Interview mode configuration page."""
    return render_template("hr_interview.html")


@interview_bp.route("/technical")
@login_required
def technical():
    """Renders Technical Interview category selection page."""
    return render_template("technical_interview.html")


@interview_bp.route("/coding")
@login_required
def coding():
    """Renders Coding Interview environment configuration page."""
    return render_template("coding_interview.html")


@interview_bp.route("/company")
@login_required
def company():
    """Renders Company-Specific Interview selection page."""
    return render_template("company_interview.html")


@interview_bp.route("/generate", methods=["POST"])
@login_required
def generate():
    """Generates an interview session and question set based on selected criteria."""
    interview_type = request.form.get("interview_type", "hr").lower()
    category = request.form.get("category", "")
    company_name = request.form.get("company_name", "")
    difficulty = request.form.get("difficulty", "medium").lower()

    # Load candidate resume parsed data if available for resume-based questions
    latest_resume = Resume.query.filter_by(user_id=current_user.id, is_active=True).order_by(Resume.upload_date.desc()).first()
    resume_data = None
    if latest_resume:
        analysis = ResumeAnalysis.query.filter_by(resume_id=latest_resume.id).first()
        if analysis:
            resume_data = analysis.get_parsed_data()

    # Generate questions using AI engine
    generator = QuestionGenerator()
    q_data_list = generator.generate_questions(
        interview_type=interview_type,
        category=category,
        company_name=company_name,
        difficulty=difficulty,
        resume_data=resume_data,
        count=5
    )

    try:
        # Create Interview DB Record
        new_interview = Interview(
            user_id=current_user.id,
            interview_type=interview_type,
            company_name=company_name if company_name else None,
            category=category if category else None,
            difficulty=difficulty,
            total_questions=len(q_data_list),
            status="in_progress"
        )
        db.session.add(new_interview)
        db.session.commit()

        # Create Question DB Records
        for q_item in q_data_list:
            question_rec = Question(
                interview_id=new_interview.id,
                question_text=q_item["question_text"],
                category=q_item["category"],
                difficulty=q_item["difficulty"],
                expected_answer=q_item["expected_answer"]
            )
            db.session.add(question_rec)

        db.session.commit()

        current_app.logger.info(f"Interview #{new_interview.id} ({interview_type}) generated for User #{current_user.id}.")
        return redirect(url_for("interview.room", interview_id=new_interview.id))

    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error generating interview for User #{current_user.id}: {str(e)}")
        flash("An error occurred while generating interview questions.", "danger")
        return redirect(url_for("interview.select"))


@interview_bp.route("/room/<int:interview_id>")
@login_required
def room(interview_id: int):
    """Renders interactive AI Interview Room."""
    interview_obj = Interview.query.filter_by(id=interview_id, user_id=current_user.id).first_or_404()
    questions = Question.query.filter_by(interview_id=interview_obj.id).order_by(Question.id.asc()).all()

    # Map existing answers
    existing_answers = Answer.query.filter_by(interview_id=interview_obj.id).all()
    answers_map = {ans.question_id: ans for ans in existing_answers}

    return render_template(
        "interview_room.html",
        interview=interview_obj,
        questions=questions,
        answers_map=answers_map
    )


@interview_bp.route("/answer", methods=["POST"])
@login_required
def submit_answer():
    """Evaluates candidate response via AI and stores Answer record."""
    data = request.get_json(silent=True) or request.form

    interview_id = data.get("interview_id")
    question_id = data.get("question_id")
    user_answer = data.get("user_answer", "").strip()
    code_language = data.get("code_language", "")

    if not interview_id or not question_id:
        return jsonify({"success": False, "error": "Missing interview or question parameters."}), 400

    interview_obj = Interview.query.filter_by(id=interview_id, user_id=current_user.id).first_or_404()
    question_obj = Question.query.filter_by(id=question_id, interview_id=interview_obj.id).first_or_404()

    # Code execution check if coding interview
    code_output_text = ""
    if interview_obj.interview_type == "coding" and user_answer:
        coding_svc = CodingService()
        exec_res = coding_svc.execute_python_code(user_answer)
        code_output_text = f"\n\n[Code Execution Output]:\n{exec_res.get('output')}"

    # AI Evaluation
    evaluator = AnswerEvaluator()
    eval_res = evaluator.evaluate_answer(
        question_text=question_obj.question_text,
        expected_answer=question_obj.expected_answer,
        user_answer=user_answer + code_output_text,
        difficulty=interview_obj.difficulty
    )

    try:
        # Check if answer record exists (update or create)
        answer_rec = Answer.query.filter_by(question_id=question_obj.id, interview_id=interview_obj.id).first()
        if not answer_rec:
            answer_rec = Answer(
                question_id=question_obj.id,
                interview_id=interview_obj.id,
                user_answer=user_answer,
                code_language=code_language
            )

        answer_rec.user_answer = user_answer
        answer_rec.answer_score = eval_res["overall_score"]
        answer_rec.technical_score = eval_res["technical_score"]
        answer_rec.communication_score = eval_res["communication_score"]
        answer_rec.relevance_score = eval_res["relevance_score"]
        answer_rec.feedback = eval_res["feedback"]
        answer_rec.strengths = eval_res["strengths"]
        answer_rec.improvements = eval_res["improvements"]

        db.session.add(answer_rec)
        db.session.commit()

        current_app.logger.info(f"Answer submitted for Question #{question_id} in Interview #{interview_id}. Score: {eval_res['overall_score']}")

        return jsonify({
            "success": True,
            "score": eval_res["overall_score"],
            "technical_score": eval_res["technical_score"],
            "communication_score": eval_res["communication_score"],
            "relevance_score": eval_res["relevance_score"],
            "feedback": eval_res["feedback"],
            "strengths": eval_res["strengths"],
            "improvements": eval_res["improvements"],
            "code_output": code_output_text
        })

    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error saving answer for Question #{question_id}: {str(e)}")
        return jsonify({"success": False, "error": str(e)}), 500


@interview_bp.route("/upload_audio", methods=["POST"])
@login_required
def upload_audio():
    """Handles audio response upload from speech microphone recorder."""
    if "audio_file" not in request.files:
        return jsonify({"success": False, "error": "No audio file uploaded."}), 400

    audio_file = request.files["audio_file"]
    interview_id = request.form.get("interview_id")
    question_id = request.form.get("question_id")
    transcript_text = request.form.get("transcript_text", "")

    try:
        speech_svc = SpeechService()
        rel_path = speech_svc.save_audio_file(current_user.id, interview_id, question_id, audio_file)
        final_transcript = speech_svc.process_speech_transcript(transcript_text, rel_path)

        current_app.logger.info(f"Audio recorded & transcript saved for User #{current_user.id}: {rel_path}")

        return jsonify({
            "success": True,
            "audio_path": rel_path,
            "transcript": final_transcript
        })
    except Exception as e:
        current_app.logger.error(f"Error handling audio upload: {str(e)}")
        return jsonify({"success": False, "error": str(e)}), 500


@interview_bp.route("/complete/<int:interview_id>", methods=["GET", "POST"])
@login_required
def complete(interview_id: int):
    """Completes interview session, computes final score, and builds PDF report."""
    interview_obj = Interview.query.filter_by(id=interview_id, user_id=current_user.id).first_or_404()
    questions = Question.query.filter_by(interview_id=interview_obj.id).all()
    answers = Answer.query.filter_by(interview_id=interview_obj.id).all()

    answers_dict = {ans.question_id: ans for ans in answers}

    # Calculate average overall score
    if answers:
        avg_score = int(sum(ans.answer_score for ans in answers) / len(answers))
    else:
        avg_score = 0

    interview_obj.score = avg_score
    interview_obj.status = "completed"
    interview_obj.completed_at = datetime.utcnow()
    db.session.commit()

    # Generate PDF Report
    try:
        report_svc = InterviewReportService()
        rel_report_path = report_svc.generate_pdf_report(current_user.fullname, interview_obj, questions, answers_dict)
        interview_obj.report_path = rel_report_path
        db.session.commit()
    except Exception as e:
        current_app.logger.error(f"Error generating PDF report for Interview #{interview_id}: {str(e)}")

    current_app.logger.info(f"Interview #{interview_id} completed. Final Score: {avg_score}")
    flash("Interview completed successfully!", "success")

    return redirect(url_for("interview.result", interview_id=interview_obj.id))


@interview_bp.route("/result/<int:interview_id>")
@login_required
def result(interview_id: int):
    """Renders comprehensive performance result report for completed interview."""
    interview_obj = Interview.query.filter_by(id=interview_id, user_id=current_user.id).first_or_404()
    questions = Question.query.filter_by(interview_id=interview_obj.id).all()
    answers = Answer.query.filter_by(interview_id=interview_obj.id).all()
    answers_dict = {ans.question_id: ans for ans in answers}

    return render_template(
        "interview_result.html",
        interview=interview_obj,
        questions=questions,
        answers_map=answers_dict
    )


@interview_bp.route("/download_report/<int:interview_id>")
@login_required
def download_report(interview_id: int):
    """Downloads generated PDF interview report."""
    interview_obj = Interview.query.filter_by(id=interview_id, user_id=current_user.id).first_or_404()

    if not interview_obj.report_path:
        flash("PDF report not available.", "warning")
        return redirect(url_for("interview.result", interview_id=interview_id))

    abs_path = os.path.abspath(os.path.join(current_app.root_path, "..", interview_obj.report_path))

    if not os.path.exists(abs_path):
        flash("PDF report file not found on server.", "danger")
        return redirect(url_for("interview.result", interview_id=interview_id))

    return send_file(abs_path, as_attachment=True, download_name=f"Interview_Report_{interview_id}.pdf")

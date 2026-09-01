"""
Company portal routes for the AI Interview Coach platform.

Provides web endpoints for browsing company profiles and
accessing company-specific interview preparation materials.
"""
from flask import Blueprint, render_template, jsonify, request
from flask_login import login_required

from backend.database import db
from backend.models.company import Company

company_bp = Blueprint("company", __name__, url_prefix="/company")


@company_bp.route("/")
@login_required
def company_list():
    """Render the company directory page."""
    companies = Company.query.order_by(Company.name.asc()).all()
    return render_template("company/index.html", companies=companies)


@company_bp.route("/<int:company_id>")
@login_required
def company_detail(company_id: int):
    """Render detail page for a specific company."""
    company = Company.query.get_or_404(company_id)
    return render_template("company/detail.html", company=company)


@company_bp.route("/api/list")
@login_required
def api_company_list():
    """Return a JSON list of all company profiles."""
    companies = Company.query.order_by(Company.name.asc()).all()
    return jsonify({
        "success": True,
        "total": len(companies),
        "companies": [c.to_dict() for c in companies],
    })


@company_bp.route("/api/search")
@login_required
def api_company_search():
    """
    Search companies by name or industry.

    Query params: ``q`` (search term), ``industry`` (optional filter)
    """
    query = request.args.get("q", "").strip()
    industry = request.args.get("industry", "").strip()

    qs = Company.query
    if query:
        qs = qs.filter(Company.name.ilike(f"%{query}%"))
    if industry:
        qs = qs.filter(Company.industry.ilike(f"%{industry}%"))

    companies = qs.order_by(Company.name.asc()).limit(50).all()
    return jsonify({
        "success": True,
        "query": query,
        "total": len(companies),
        "companies": [c.to_dict() for c in companies],
    })

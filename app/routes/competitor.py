from flask import Blueprint, render_template

competitor_bp = Blueprint("competitor", __name__)

@competitor_bp.route("/competitor")
def competitor_page():
    return render_template("competitor.html")
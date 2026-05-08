from flask import Blueprint, render_template, jsonify

competitor_bp = Blueprint("competitor", __name__)

@competitor_bp.route("/competitor")
def competitor_page():
    return render_template("competitor.html")


@competitor_bp.route("/api/competitors")
def competitor_api():

    data = [
        {
            "name": "Apple",
            "pos": 61,
            "neu": 24,
            "neg": 15,
            "score": 7.4,
            "articles": 2841
        },
        {
            "name": "Google",
            "pos": 58,
            "neu": 28,
            "neg": 14,
            "score": 6.9,
            "articles": 3102
        },
        {
            "name": "Microsoft",
            "pos": 55,
            "neu": 31,
            "neg": 14,
            "score": 6.5,
            "articles": 1987
        },
        {
            "name": "Tesla",
            "pos": 38,
            "neu": 22,
            "neg": 40,
            "score": 4.2,
            "articles": 4210
        }
    ]

    return jsonify(data)
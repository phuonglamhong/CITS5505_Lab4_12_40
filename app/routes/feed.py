"""
routes/feed.py — Media Feed blueprint
Task 3: Media Feed route with article query, filter and search logic
"""

from flask import Blueprint, render_template, request, session, redirect, url_for
from app.models.article import Article

feed_bp = Blueprint("feed", __name__)


@feed_bp.route("/feed")
def feed():
    # Redirect to login if not logged in
    if "user_id" not in session:
        return redirect(url_for("users.index"))

    # Get filter parameters from URL
    active_filter = request.args.get("sentiment", "all")
    active_source = request.args.get("source", "")
    search_query  = request.args.get("q", "")

    # Base query
    query = Article.query

    # Filter by sentiment
    if active_filter in ("positive", "neutral", "negative"):
        query = query.filter_by(sentiment=active_filter)

    # Filter by source
    if active_source:
        query = query.filter_by(source=active_source)

    # Search by title
    if search_query:
        query = query.filter(Article.title.ilike(f"%{search_query}%"))

    articles = query.order_by(Article.date.desc()).all()

    # Count stats
    all_articles = Article.query.all()
    counts = {
        "total":    len(all_articles),
        "positive": sum(1 for a in all_articles if a.sentiment == "positive"),
        "neutral":  sum(1 for a in all_articles if a.sentiment == "neutral"),
        "negative": sum(1 for a in all_articles if a.sentiment == "negative"),
    }

    return render_template(
        "feed.html",
        articles=articles,
        counts=counts,
        active_filter=active_filter,
        active_source=active_source,
        search_query=search_query,
    )

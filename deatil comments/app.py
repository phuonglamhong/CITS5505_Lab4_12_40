from flask import Flask, request, jsonify, render_template, redirect, url_for
import sqlite3
from datetime import datetime

app = Flask(__name__)
DB_NAME = "comments.db"


def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db_connection()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS comments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            article_id INTEGER NOT NULL,
            author TEXT NOT NULL,
            time TEXT NOT NULL,
            tag TEXT,
            body TEXT NOT NULL
        )
    """)

    existing = conn.execute(
        "SELECT COUNT(*) AS count FROM comments WHERE article_id = ?",
        (2,)
    ).fetchone()["count"]

    if existing == 0:
        conn.execute("""
            INSERT INTO comments (article_id, author, time, tag, body)
            VALUES (?, ?, ?, ?, ?)
        """, (
            2,
            "Jordan Lee",
            "2h ago",
            "Misclassified",
            "This feels over-classified as negative. The contingency section is genuinely positive — it may be dragging the overall score down unfairly."
        ))

        conn.execute("""
            INSERT INTO comments (article_id, author, time, tag, body)
            VALUES (?, ?, ?, ?, ?)
        """, (
            2,
            "Sara Mitchell",
            "45m ago",
            "Flagged",
            "Escalating this to the crisis monitoring queue. 847 social mentions in 2 hours is significant."
        ))

    conn.commit()
    conn.close()


@app.route("/")
def home():
    return redirect(url_for("detail", article_id=2))


@app.route("/detail/<int:article_id>")
def detail(article_id):
    return render_template("detail.html", article_id=article_id)


@app.route("/api/articles/<int:article_id>/comments", methods=["GET", "POST"])
def article_comments(article_id):
    conn = get_db_connection()

    if request.method == "GET":
        rows = conn.execute("""
            SELECT author, time, tag, body
            FROM comments
            WHERE article_id = ?
            ORDER BY id ASC
        """, (article_id,)).fetchall()

        conn.close()
        comments = [dict(row) for row in rows]
        return jsonify(comments)

    data = request.get_json() or {}
    body = data.get("body", "").strip()
    tag = data.get("tag", "").strip()

    if not body:
        conn.close()
        return jsonify({"error": "Comment body is required."}), 400

    time_str = datetime.now().strftime("%Y-%m-%d %H:%M")

    conn.execute("""
        INSERT INTO comments (article_id, author, time, tag, body)
        VALUES (?, ?, ?, ?, ?)
    """, (
        article_id,
        "Alex Chen",
        time_str,
        tag,
        body
    ))

    conn.commit()
    conn.close()

    return jsonify({
        "author": "Alex Chen",
        "time": time_str,
        "tag": tag,
        "body": body
    }), 201


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
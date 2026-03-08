from flask import Flask, request, render_template_string, redirect
import yt_dlp
import os

app = Flask(__name__)

# UI එක ටිකක් ලස්සනට සහ සිංහලෙන්
html_template = """
<!DOCTYPE html>
<html lang="si">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>YT Downloader - DrapXi Projects</title>
    <style>
        body { font-family: 'Segoe UI', sans-serif; display: flex; justify-content: center; align-items: center; height: 100vh; background: #0f172a; color: white; margin: 0; }
        .container { background: #1e293b; padding: 40px; border-radius: 15px; box-shadow: 0 10px 25px rgba(0,0,0,0.3); text-align: center; width: 90%; max-width: 450px; border: 1px solid #334155; }
        h2 { margin-bottom: 25px; color: #38bdf8; font-size: 24px; }
        input[type="text"] { width: 100%; padding: 12px; margin-bottom: 20px; border: 1px solid #334155; border-radius: 8px; background: #0f172a; color: white; box-sizing: border-box; outline: none; }
        input[type="text"]:focus { border-color: #38bdf8; }
        button { background-color: #ef4444; color: white; border: none; padding: 12px 25px; border-radius: 8px; cursor: pointer; font-weight: bold; width: 100%; transition: 0.3s; font-size: 16px; }
        button:hover { background-color: #dc2626; transform: translateY(-2px); }
        .footer { font-size: 12px; color: #94a3b8; margin-top: 25px; border-top: 1px solid #334155; padding-top: 15px; }
        .error { color: #f87171; background: #450a0a; padding: 10px; border-radius: 5px; margin-bottom: 15px; font-size: 14px; display: none; }
    </style>
</head>
<body>
    <div class="container">
        <h2>YouTube Downloader</h2>
        <form action="/download" method="get">
            <input type="text" name="url" placeholder="Paste YouTube Link Here..." required>
            <button type="submit">Download Now</button>
        </form>
        <div class="footer">
            Developed by <b>Ositha</b> | Powered by DrapXi & Vercel
        </div>
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(html_template)

@app.route('/download')
def download_video():
    video_url = request.args.get('url')
    if not video_url:
        return "කරුණාකර Link එකක් ඇතුළත් කරන්න!", 400

    # Cookie file එක තියෙනවද බලන්න
    cookie_path = 'cookies.txt'
    
    ydl_opts = {
        'format': 'best',
        'noplaylist': True,
        'quiet': True,
        # User Agent එක මගින් සැබෑ browser එකක් බව අඟවයි
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

    # Cookies තිබේ නම් පමණක් භාවිතා කරයි
    if os.path.exists(cookie_path):
        ydl_opts['cookiefile'] = cookie_path

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # වීඩියෝ තොරතුරු ලබාගන්න (download නොකර)
            info = ydl.extract_info(video_url, download=False)
            # Direct Download Link එකට redirect කරන්න
            download_url = info.get('url')
            
            if download_url:
                return redirect(download_url)
            else:
                return "වීඩියෝ එකේ Link එක ලබා ගැනීමට නොහැකි විය.", 404
                
    except Exception as e:
        error_msg = str(e)
        # Error එක සරලව පෙන්වන්න
        if "Sign in to confirm" in error_msg:
            return "YouTube විසින් සර්වර් එක Block කර ඇත. කරුණාකර cookies.txt එක අලුත් කරන්න.", 403
        return f"වැරැද්දක් සිදු වුණා: {error_msg}", 500

if __name__ == '__main__':
    app.run(debug=True)

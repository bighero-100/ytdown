from flask import Flask, request, render_template_string, redirect
import yt_dlp

app = Flask(__name__)

html_template = """
<!DOCTYPE html>
<html lang="si">
<head>
    <meta charset="UTF-8">
    <title>YT Downloader - DrapXi Projects</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; display: flex; justify-content: center; align-items: center; height: 100vh; background: #0f172a; color: white; margin: 0; }
        .container { background: #1e293b; padding: 40px; border-radius: 15px; box-shadow: 0 10px 25px rgba(0,0,0,0.3); text-align: center; width: 450px; border: 1px solid #334155; }
        h2 { margin-bottom: 25px; color: #38bdf8; }
        input[type="text"] { width: 100%; padding: 12px; margin-bottom: 20px; border: 1px solid #334155; border-radius: 8px; background: #0f172a; color: white; box-sizing: border-box; }
        button { background-color: #ef4444; color: white; border: none; padding: 12px 25px; border-radius: 8px; cursor: pointer; font-weight: bold; width: 100%; transition: 0.3s; }
        button:hover { background-color: #dc2626; transform: translateY(-2px); }
        .footer { font-size: 12px; color: #94a3b8; margin-top: 20px; }
    </style>
</head>
<body>
    <div class="container">
        <h2>YouTube Downloader</h2>
        <form action="/download" method="get">
            <input type="text" name="url" placeholder="Paste YouTube Link Here..." required>
            <button type="submit">Get Download Link</button>
        </form>
        <div class="footer">Powered by yt-dlp & Vercel</div>
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

    ydl_opts = {
        'format': 'best',
        'noplaylist': True,
        'quiet': True
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            # කෙලින්ම download කළ හැකි URL එක ලබා ගැනීම
            download_url = info.get('url')
            return redirect(download_url)
    except Exception as e:
        return f"වැරැද්දක් සිදු වුණා: {str(e)}", 500

if __name__ == '__main__':
    app.run(debug=True)
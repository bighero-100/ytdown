from flask import Flask, request, render_template_string, redirect
import yt_dlp
import os

app = Flask(__name__)

# UI එක (HTML/CSS)
html_template = """
<!DOCTYPE html>
<html lang="si">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>YT Downloader - DrapXi</title>
    <style>
        body { font-family: 'Segoe UI', sans-serif; display: flex; justify-content: center; align-items: center; height: 100vh; background: #0f172a; color: white; margin: 0; }
        .container { background: #1e293b; padding: 40px; border-radius: 15px; box-shadow: 0 10px 25px rgba(0,0,0,0.3); text-align: center; width: 90%; max-width: 400px; border: 1px solid #334155; }
        h2 { margin-bottom: 25px; color: #38bdf8; font-size: 24px; }
        input[type="text"] { width: 100%; padding: 12px; margin-bottom: 20px; border: 1px solid #334155; border-radius: 8px; background: #0f172a; color: white; box-sizing: border-box; outline: none; }
        button { background-color: #ef4444; color: white; border: none; padding: 12px 25px; border-radius: 8px; cursor: pointer; font-weight: bold; width: 100%; transition: 0.3s; font-size: 16px; }
        button:hover { background-color: #dc2626; transform: translateY(-2px); }
        .footer { font-size: 12px; color: #94a3b8; margin-top: 25px; border-top: 1px solid #334155; padding-top: 15px; }
    </style>
</head>
<body>
    <div class="container">
        <h2>YouTube Downloader</h2>
        <form action="/download" method="get">
            <input type="text" name="url" placeholder="Paste YouTube Link Here..." required>
            <button type="submit">Download Video</button>
        </form>
        <div class="footer">Developed by Ositha | Powered by DrapXi</div>
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

    # Vercel එකේ cookies.txt තියෙන තැන නිවැරදිව හඳුනා ගැනීම
    # මෙය Read-only error එක වළක්වා ගැනීමට උපකාරී වේ
    base_path = os.path.dirname(os.path.abspath(__file__))
    cookie_path = os.path.join(base_path, 'cookies.txt')

    ydl_opts = {
        'format': 'best',
        'noplaylist': True,
        'quiet': True,
        'no_warnings': True,
        # Cookies කියවීමට පමණක් (Read Only) ලබා දීම
        'cookiefile': cookie_path if os.path.exists(cookie_path) else None,
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # තොරතුරු ලබා ගැනීම පමණයි කරන්නේ (No Downloading to server)
            info = ydl.extract_info(video_url, download=False)
            download_url = info.get('url')
            
            if download_url:
                # කෙලින්ම Video Link එකට redirect කරයි
                return redirect(download_url)
            else:
                return "වීඩියෝව සොයාගත නොහැකි විය.", 404
                
    except Exception as e:
        # වැරැද්ද පෙන්වීම
        return f"වැරැද්දක් සිදු වුණා: {str(e)}", 500

if __name__ == '__main__':
    app.run(debug=True)

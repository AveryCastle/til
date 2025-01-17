from flask import Flask, redirect, url_for, session, request
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
import google.auth.transport.requests
import os

app = Flask(__name__)
app.secret_key = "your_secret_key"  # 안전한 임의의 문자열로 변경하세요.

# Google OAuth 2.0 클라이언트 구성
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"  # HTTPS가 아닌 경우 활성화 (개발용)
CLIENT_ID = "15020443312-24hubg7t6k5kpmbv0r3v7kmq2a8b42u7.apps.googleusercontent.com"
CLIENT_SECRET = "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"
REDIRECT_URI = "http://localhost:5000/callback"

flow = Flow.from_client_secrets_file(
    'client_secret.json',  # Google Cloud Console에서 다운로드한 JSON 파일
    scopes = [
        "https://www.googleapis.com/auth/userinfo.profile",
        "https://www.googleapis.com/auth/userinfo.email",
        "openid",
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive.file"
    ],
    redirect_uri=REDIRECT_URI,
)


@app.route("/")
def index():
    return '<a href="/login">Google 계정으로 로그인</a>'


@app.route("/login")
def login():
    authorization_url, _ = flow.authorization_url(prompt="consent")
    return redirect(authorization_url)


@app.route("/callback")
def callback():
    flow.fetch_token(authorization_response=request.url)

    credentials = flow.credentials
    request_session = google.auth.transport.requests.Request()
    id_info = id_token.verify_oauth2_token(
        credentials.id_token, request_session, CLIENT_ID
    )

    session["google_id"] = id_info.get("sub")
    session["name"] = id_info.get("name")
    session["email"] = id_info.get("email")

    return f'''
        <style>
            .logout-btn {{
                position: fixed;
                top: 20px;
                right: 20px;
                padding: 10px 20px;
                background-color: #f8f9fa;
                border: 1px solid #dee2e6;
                border-radius: 4px;
                text-decoration: none;
                color: #212529;
            }}
            .logout-btn:hover {{
                background-color: #e9ecef;
            }}
        </style>
        <a href="/logout" class="logout-btn">로그아웃</a>
        <p>안녕하세요, {session['name']}님! ({session['email']})</p>
    '''


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)

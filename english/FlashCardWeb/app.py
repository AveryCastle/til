from flask import Flask, redirect, url_for, session, request, render_template, jsonify
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
import google.auth.transport.requests
import os
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from spreadsheet_manager import SpreadsheetManager
import logging  # 새로 추가

# 로깅 설정 추가
logging.basicConfig(
    filename='flashcard_error.log',
    level=logging.ERROR,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

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

def create_drive_service(credentials):
    return build('drive', 'v3', credentials=credentials)

def create_sheets_service(credentials):
    return build('sheets', 'v4', credentials=credentials)

def check_and_create_folder(drive_service, folder_name):
    query = f"name='{folder_name}' and mimeType='application/vnd.google-apps.folder' and trashed=false"
    
    try:
        results = drive_service.files().list(q=query, spaces='drive').execute()
        items = results.get('files', [])

        if not items:
            folder_metadata = {
                'name': folder_name,
                'mimeType': 'application/vnd.google-apps.folder'
            }
            folder = drive_service.files().create(body=folder_metadata, fields='id').execute()
            return folder.get('id')
        return items[0]['id']
    except HttpError as error:
        raise Exception(f'폴더 생성 중 오류 발생: {error}')

def check_and_create_spreadsheet(drive_service, sheets_service, folder_id, sheet_name):
    query = f"name='{sheet_name}' and '{folder_id}' in parents and mimeType='application/vnd.google-apps.spreadsheet' and trashed=false"
    
    try:
        results = drive_service.files().list(q=query, spaces='drive').execute()
        items = results.get('files', [])

        if not items:
            spreadsheet = {
                'properties': {'title': sheet_name}
            }
            spreadsheet = sheets_service.spreadsheets().create(body=spreadsheet).execute()
            spreadsheet_id = spreadsheet.get('spreadsheetId')

            file = drive_service.files().update(
                fileId=spreadsheet_id,
                addParents=folder_id,
                fields='id, parents'
            ).execute()

            sheet_manager = SpreadsheetManager(sheets_service, spreadsheet_id)
            sheet_manager.initialize_sheets()
            
            return spreadsheet_id
        
        spreadsheet_id = items[0]['id']
        sheet_manager = SpreadsheetManager(sheets_service, spreadsheet_id)
        sheet_manager.initialize_sheets()
        
        return spreadsheet_id
    except HttpError as error:
        raise Exception(f'스프레드시트 생성 중 오류 발생: {error}')

@app.route("/")
def index():
    if 'email' not in session:
        return redirect(url_for('login'))
    
    try:
        credentials = flow.credentials
        sheets_service = create_sheets_service(credentials)
        sheet_manager = SpreadsheetManager(sheets_service, session['spreadsheet_id'])
        
        all_data = []
        for sheet_name in ['30일', '15일', '7일', '5일', '3일', '2일', '1일']:
            sheet_data = sheet_manager.get_sheet_data(sheet_name)
            if sheet_data:
                for row in sheet_data:
                    all_data.append({
                        'day': sheet_name,
                        'english': row[0],
                        'korean': row[1],
                        'description': row[2] if len(row) > 2 else ''
                    })
        
        session['all_data'] = all_data
        return render_template('index.html', all_data=all_data)
        
    except Exception as error:
        logging.error(f"Index 페이지 에러: {str(error)}", exc_info=True)
        session.clear()
        return redirect(url_for('login'))

@app.route("/save", methods=['POST'])
def save():
    if 'google_id' not in session:
        authorization_url, _ = flow.authorization_url(prompt="consent")
        return redirect(authorization_url)

    try:
        credentials = flow.credentials
        sheets_service = create_sheets_service(credentials)
        sheet_manager = SpreadsheetManager(sheets_service, session['spreadsheet_id'])

        english = request.form.get('english')
        korean = request.form.get('korean')
        description = request.form.get('description', '')

        sheet_manager.append_to_sheet(english, korean, description)
        return redirect('/')
    except Exception as error:
        logging.error(f"저장 중 에러: {str(error)}", exc_info=True)
        session.clear()
        return redirect(url_for('login'))

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

    try:
        # 서비스 초기화
        drive_service = create_drive_service(credentials)
        sheets_service = create_sheets_service(credentials)

        # 폴더 확인 및 생성
        folder_id = check_and_create_folder(drive_service, 'FlashCardWeb_English')
        session['folder_id'] = folder_id

        # 스프레드시트 확인 및 생성
        spreadsheet_id = check_and_create_spreadsheet(
            drive_service, 
            sheets_service, 
            folder_id, 
            'English'
        )
        session['spreadsheet_id'] = spreadsheet_id

        return redirect(url_for('index'))

    except Exception as error:
        logging.error(f"콜백 처리 중 에러: {str(error)}", exc_info=True)
        session.clear()
        return redirect(url_for('login'))

@app.route('/study', methods=['POST'])
def study():
    if 'email' not in session:
        return redirect(url_for('login'))
        
    selected_language = request.form.get('selected_language')
    all_data = session.get('all_data', [])
    
    if not all_data:
        return redirect(url_for('index'))
    
    # 디버깅을 위한 출력
    print("Selected language:", selected_language)
    print("All data:", all_data)
    
    current_card = all_data[0]
    session['current_index'] = 0
    
    front_text = current_card['korean'] if selected_language == 'korean' else current_card['english']
    back_text = current_card['english'] if selected_language == 'korean' else current_card['korean']
    
    # 명시적으로 flashcard.html을 렌더링
    return render_template('flashcard.html', 
                         front_text=front_text,
                         back_text=back_text,
                         description=current_card.get('description', ''),
                         total_cards=len(all_data))

@app.route("/logout")
def logout():
    session.clear()
    return render_template('login.html')

@app.route('/next_card', methods=['POST'])
def next_card():
    all_data = session.get('all_data', [])
    current_index = session.get('current_index', 0)
    selected_language = request.form.get('selected_language')
    
    # 다음 카드 인덱스 계산
    next_index = (current_index + 1) % len(all_data)
    session['current_index'] = next_index
    
    current_card = all_data[next_index]
    front_text = current_card['korean'] if selected_language == 'korean' else current_card['english']
    back_text = current_card['english'] if selected_language == 'korean' else current_card['korean']
    
    return jsonify({
        'front_text': front_text,
        'back_text': back_text,
        'description': current_card.get('description', '')
    })

if __name__ == "__main__":
    app.debug = True
    app.run()

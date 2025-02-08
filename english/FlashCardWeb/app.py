from flask import Flask, redirect, url_for, session, request, render_template, jsonify, current_app, make_response, send_from_directory
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
import google.auth.transport.requests
import os
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from spreadsheet_manager import SpreadsheetManager
import logging  # 새로 추가
# from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, date
import pytz
from database import get_db, init_db, add_active_user, get_user_last_move_date, update_last_move_date
import traceback
from flask_talisman import Talisman  # pip install flask-talisman

# 로깅 설정 추가
logging.basicConfig(
    filename='flashcard_error.log',
    level=logging.ERROR,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# 전역 변수로 app 인스턴스를 저장
flask_app = None

def create_app():
    global flask_app
    app = Flask(__name__)
    flask_app = app
    app.secret_key = "1q2w3e4r5t6y7u8i9o0p"  # 안전한 임의의 문자열로 변경하세요.
    Talisman(app, 
        content_security_policy={
            'default-src': "'self'",
            'style-src': ["'self'", "'unsafe-inline'"],
            'script-src': ["'self'", "'unsafe-inline'", "cdn.jsdelivr.net"],
            'img-src': ["'self'", 'data:', 'https:']
        }
    )

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

    @app.route('/', methods=['GET'])
    def index():
        if 'email' not in session:
            return redirect(url_for('login'))
        
        try:
            credentials = flow.credentials
            sheets_service = create_sheets_service(credentials)
            sheet_manager = SpreadsheetManager(sheets_service, session['spreadsheet_id'])
            
            all_data = []
            for sheet_name in ['30일', '15일', '10일', '7일', '5일', '3일', '2일', '1일']:
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

    @app.route('/login', methods=['GET'])
    def login():
        authorization_url, _ = flow.authorization_url(prompt="consent")
        return redirect(authorization_url)

    @app.route('/callback', methods=['GET'])
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
            with app.app_context():
                init_db()

            drive_service = create_drive_service(credentials)
            sheets_service = create_sheets_service(credentials)

            folder_id = check_and_create_folder(drive_service, 'FlashCardWeb_English')
            session['folder_id'] = folder_id

            spreadsheet_id = check_and_create_spreadsheet(
                drive_service, 
                sheets_service, 
                folder_id, 
                'English'
            )
            session['spreadsheet_id'] = spreadsheet_id

            # database.py의 함수를 사용하여 사용자 정보 저장
            add_active_user(session['email'], spreadsheet_id)

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
        
        current_index = 0  # 초기 인덱스 설정
        current_card = all_data[current_index]
        session['current_index'] = current_index
        
        front_text = current_card['korean'] if selected_language == 'korean' else current_card['english']
        back_text = current_card['english'] if selected_language == 'korean' else current_card['korean']
        
        return render_template('flashcard.html', 
                             front_text=front_text,
                             back_text=back_text,
                             description=current_card.get('description', ''),
                             total_cards=len(all_data),
                             selected_language=selected_language,
                             current_index=current_index,  # current_index 추가
                             all_data=all_data)  # all_data도 함께 전달

    @app.route("/logout")
    def logout():
        session.clear()
        return render_template('login.html')

    @app.route('/next_card', methods=['POST'])
    def next_card():
        data = request.get_json()
        all_data = session.get('all_data', [])
        current_index = data.get('current_index', 0)
        selected_language = data.get('selected_language')
        
        if 0 <= current_index < len(all_data):
            current_card = all_data[current_index]
            front_text = current_card['korean'] if selected_language == 'korean' else current_card['english']
            back_text = current_card['english'] if selected_language == 'korean' else current_card['korean']
            
            return jsonify({
                'front_text': front_text,
                'back_text': back_text,
                'description': current_card.get('description', ''),
                'current_index': current_index
            })
        
        return jsonify({'error': 'Invalid index'}), 400

    @app.route('/flashcard')
    def flashcard():
        if 'all_data' not in session:
            return redirect(url_for('index'))
        
        current_index = request.args.get('index', 0, type=int)
        all_data = session['all_data']
        
        # 인덱스가 범위를 벗어나지 않도록 보정
        if current_index < 0:
            current_index = 0
        elif current_index >= len(all_data):
            current_index = len(all_data) - 1
        
        return render_template('flashcard.html', 
                             all_data=all_data,
                             current_index=current_index)

    @app.route('/add_expression_form')
    def add_expression_form():
        if 'email' not in session:
            return redirect(url_for('login'))
        
        try:
            credentials = flow.credentials
            sheets_service = create_sheets_service(credentials)
            sheet_manager = SpreadsheetManager(sheets_service, session['spreadsheet_id'])
            expressions = sheet_manager.get_sheet_data('1일')
            return render_template('add_expression.html', expressions=expressions)
        except Exception as error:
            logging.error(f"표현 조회 중 에러: {str(error)}", exc_info=True)
            return redirect(url_for('index'))

    @app.route('/save_expression', methods=['POST'])
    def save_expression():
        if 'email' not in session:
            return jsonify({'success': False, 'error': 'Not logged in'})
        
        try:
            credentials = flow.credentials
            sheets_service = create_sheets_service(credentials)
            sheet_manager = SpreadsheetManager(sheets_service, session['spreadsheet_id'])
            
            english = request.form.get('english')
            korean = request.form.get('korean')
            description = request.form.get('description', '')
            row_id = request.form.get('rowId')
            
            if row_id:  # 수정
                sheet_manager.update_row('1일', int(row_id), english, korean, description)
            else:  # 새로운 등록
                sheet_manager.append_to_sheet('1일', english, korean, description)
            
            return jsonify({'success': True})
        except Exception as error:
            logging.error(f"표현 저장 중 에러: {str(error)}", exc_info=True)
            return jsonify({'success': False, 'error': str(error)})

    @app.route('/delete_expression', methods=['POST'])
    def delete_expression():
        if 'email' not in session:
            return jsonify({'success': False, 'error': 'Not logged in'})
        
        try:
            credentials = flow.credentials
            sheets_service = create_sheets_service(credentials)
            sheet_manager = SpreadsheetManager(sheets_service, session['spreadsheet_id'])
            
            data = request.get_json()
            row_id = int(data.get('rowId'))
            
            sheet_manager.delete_row('1일', row_id)
            
            return jsonify({'success': True})
        except Exception as error:
            logging.error(f"표현 삭제 중 에러: {str(error)}", exc_info=True)
            return jsonify({'success': False, 'error': str(error)})

    @app.route('/check_move_status', methods=['GET'])
    def check_move_status():
        if 'email' not in session:
            return jsonify({'error': 'Not logged in'}), 401
        
        try:
            last_move_date = get_user_last_move_date(session['email'])
            today = datetime.now().strftime('%Y-%m-%d')
            
            moved_today = (last_move_date == today)
            print(f"moved_today: {moved_today}, last_move_date: {last_move_date}, today: {today}")
            return jsonify({
                'moved_today': moved_today,
                'last_move_date': last_move_date
            })
            
        except Exception as e:
            logging.error(f"Error checking move status: {str(e)}")
            return jsonify({'error': str(e)}), 500

    @app.route('/complete_study', methods=['POST'])
    def complete_study():
        if 'email' not in session:
            return jsonify({'success': False, 'error': 'Not logged in'})
        
        try:
            user_email = session['email']
            korea_tz = pytz.timezone('Asia/Seoul')
            today = datetime.now(korea_tz).date()
            
            # 사용자의 마지막 이동 날짜 확인
            last_move_date = get_user_last_move_date(user_email)
            if last_move_date == today.isoformat():
                return jsonify({
                    'success': False, 
                    'error': '오늘은 이미 학습을 완료하셨습니다. 내일 다시 시도해주세요.'
                })
            
            # 데이터 이동 실행
            credentials = flow.credentials
            sheets_service = create_sheets_service(credentials)
            sheet_manager = SpreadsheetManager(sheets_service, session['spreadsheet_id'])
            sheet_manager.move_data_to_next_day()
            
            # 마지막 이동 날짜 업데이트 (한국 시간 기준)
            update_last_move_date(user_email, today.isoformat())
            
            return jsonify({'success': True})
            
        except Exception as error:
            logging.error(f"학습 완료 처리 중 에러: {str(error)}", exc_info=True)
            return jsonify({'success': False, 'error': str(error)})

    def save_user_spreadsheet(email, spreadsheet_id):
        """사용자 스프레드시트 정보 저장"""
        db = get_db()
        db.execute(
            'INSERT OR REPLACE INTO active_users (email, spreadsheet_id) VALUES (?, ?)',
            (email, spreadsheet_id)
        )
        db.commit()

    def active_users_spreadsheets():
        """활성 사용자 정보 조회"""
        db = get_db()
        return db.execute('SELECT email, spreadsheet_id FROM active_users').fetchall()

    def get_user_credentials(user_email):
        # For now, just return the current flow's credentials
        return flow.credentials

    @app.route('/static/sw.js', methods=['GET'])
    def serve_sw():
        response = make_response(send_from_directory('static', 'sw.js'))
        response.headers['Content-Type'] = 'application/javascript'
        return response

    # manifest.json을 서빙하기 위한 라우트 추가
    @app.route('/static/manifest.json', methods=['GET'])
    def serve_manifest():
        response = make_response(send_from_directory('static', 'manifest.json'))
        response.headers['Content-Type'] = 'application/json'
        return response

    return app

if __name__ == "__main__":
     app = create_app()
     # 로컬 개발 환경에서만 실행되는 코드
     if os.environ.get('FLASK_ENV') == 'development' or os.environ.get('FLASK_ENV'):
         app.debug = True
         app.run(ssl_context='adhoc')
     else:
         # Production 환경(Python Anywhere)에서는 이 부분이 실행되지 않음
         app.run()

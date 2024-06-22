import sqlite3
from datetime import datetime
import os

# 데이터베이스 파일 경로 지정
db_path = os.path.join(os.path.dirname(__file__), '..', 'befriends.db')

# 데이터베이스 연결
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# 새로운 테이블 생성 (이미 생성되어 있으면 무시됨)
cursor.executescript('''
CREATE TABLE IF NOT EXISTS auth_methods (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    auth_type TEXT NOT NULL CHECK(auth_type IN ('telegram', 'email')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS email_auth (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    auth_method_id INTEGER NOT NULL,
    email_address TEXT NOT NULL,
    password TEXT NOT NULL,
    FOREIGN KEY (auth_method_id) REFERENCES auth_methods (id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS telegram_auth (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    auth_method_id INTEGER NOT NULL,
    telegram_id TEXT NOT NULL,
    first_name TEXT,
    last_name TEXT,
    FOREIGN KEY (auth_method_id) REFERENCES auth_methods (id) ON DELETE CASCADE
);

''')

# 모든 사용자 데이터를 가져오기
cursor.execute("SELECT id, email, password FROM users")
users = cursor.fetchall()

# 마이그레이션 함수
def migrate_user(user_id, email, password):
    # auth_methods 테이블에 이메일 인증 방법 추가
    cursor.execute("INSERT INTO auth_methods (user_id, auth_type, created_at, updated_at) VALUES (?, ?, ?, ?)",
                   (user_id, 'email', datetime.now(), datetime.now()))
    auth_method_id = cursor.lastrowid

    # email_auth 테이블에 이메일 인증 정보 추가
    cursor.execute("INSERT INTO email_auth (auth_method_id, email_address, password) VALUES (?, ?, ?)",
                   (auth_method_id, email, password))


# 새로운 테이블 생성 및 데이터 마이그레이션 함수 정의
def migrate_user_table():
    # 새로운 users 테이블 생성 (임시 테이블로 생성)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS new_users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        thread_id TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    # 기존 users 테이블에서 데이터 복사
    cursor.execute('''
    INSERT INTO new_users (id, thread_id, created_at, updated_at)
    SELECT id, thread_id, created_at, updated_at FROM users
    ''')

    # 기존 users 테이블 삭제
    cursor.execute('DROP TABLE users')

    # 새로운 users 테이블 이름 변경
    cursor.execute('ALTER TABLE new_users RENAME TO users')

# 각 사용자 데이터 마이그레이션
for user in users:
    user_id, email, password = user
    print(user_id, email, password)
    migrate_user(user_id, email, password)


# users 테이블에서 email 및 password 컬럼을 제거
migrate_user_table()


# 변경사항 저장 및 연결 종료
conn.commit()
conn.close()

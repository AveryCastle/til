import hashlib
import sqlite3

class UserManager:
    def __init__(self, db_manager):
        self.conn = db_manager.conn

    def _hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def _check_user_email(self, email, password):
        c = self.conn.cursor()
        # email_auth 테이블에서 이메일과 일치하는 레코드 찾기
        c.execute("SELECT user_id, password FROM email_auth WHERE email_address=?", (email,))
        row = c.fetchone()
        
        if not row:
            return None

        user_id, stored_password = row
        if stored_password != self._hash_password(password):
            return "Incorrect password"

        # users 테이블에서 해당 사용자의 id와 thread_id 조회
        c.execute("SELECT id, thread_id FROM users WHERE id=?", (user_id,))
        user_row = c.fetchone()
        
        return user_row if user_row else None
    

    def create_user_email(self, email, password):
        try:
            user_id = self._insert_user()
            auth_method_id = self._insert_auth_method(user_id, 'email')
            self._insert_email_auth(user_id, auth_method_id, email, password)
            print(f"New user created. User id: {user_id}")
            return user_id
        except sqlite3.IntegrityError as e:
            print(f"Error creating user: {e}")
            self.conn.rollback()
            return None
    
    def _insert_user(self):
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO users DEFAULT VALUES"
        )
        self.conn.commit()
        return cursor.lastrowid

    def _insert_auth_method(self, user_id, auth_type):
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO auth_methods (user_id, auth_type) VALUES (?, ?)",
            (user_id, auth_type)
        )
        self.conn.commit()
        return cursor.lastrowid

    def _insert_email_auth(self, user_id, auth_method_id, email, password):
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO email_auth (user_id, auth_method_id, email_address, password) VALUES (?, ?, ?, ?)",
            (user_id, auth_method_id, email, self._hash_password(password))
        )
        self.conn.commit()

    def update_thread_id(self, user_id, thread_id):
        c = self.conn.cursor()
        c.execute("UPDATE users SET thread_id=? WHERE id=?", (thread_id, user_id))
        self.conn.commit()
    
    # 텔레그램 인증 정보 추가 함수
    def _add_telegram_auth(self, auth_method_id, telegram_id, first_name, last_name):
        c = self.conn.cursor()
        c.execute("INSERT INTO telegram_auth (auth_method_id, telegram_id, first_name, last_name) VALUES (?, ?, ?, ?)",
                    (auth_method_id, telegram_id, first_name, last_name))
    
    def _email_auth(self):
        email = input("Enter email: ")
        password = input("Enter password: ")

        user_check = self._check_user_email(email, password)
        if user_check is None:
            id = self.create_user_email(email, password)
            print("New user created. User id: ", id)
            return id, None
        elif user_check == "Incorrect password":
            print(user_check)
            return None, None
        else:
            print("Existing user. User id and thread_id: ", user_check)
            return user_check
        
    def _telegram_auth(self):
        pass

    def user_input(self, auth_method):
        if auth_method == "1":
            return self._email_auth()
        elif auth_method == "2":
            return self._telegram_auth()
        else:
            print("Invalid authentication method")
            return None, None
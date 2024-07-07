import hashlib
import sqlite3
from datetime import datetime

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
        
    def register_telegram_user(self, telegram_id, first_name, last_name, username):
        try:
            user_id = self._insert_user()
            auth_method_id = self._insert_auth_method(user_id, 'telegram')
            self._insert_telegram_auth(user_id, auth_method_id, telegram_id, first_name, last_name, username)
            return user_id, None
        except sqlite3.IntegrityError as e:
            print(f"Error registering user: {e}")
            self.conn.rollback()
            return None, None  
    
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
        
    def _insert_telegram_auth(self, user_id, auth_method_id, telegram_id, first_name, last_name, username):
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO telegram_auth (user_id, auth_method_id, telegram_id, first_name, last_name, username) VALUES (?, ?, ?, ?, ?, ?)",
            (user_id, auth_method_id, telegram_id, first_name, last_name, username)
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
        
    def telegram_auth(self, telegram_id):
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                SELECT u.id, u.thread_id
                FROM users u
                JOIN telegram_auth ta ON u.id = ta.user_id
                WHERE ta.telegram_id = ?
            """, (telegram_id,))
            row = cursor.fetchone()
            if row:
                return row  # (id, thread_id)
            return None
        except sqlite3.Error as e:
            print(e)
            return None

    def user_input(self, auth_method):
        if auth_method == "1":
            return self._email_auth()
        elif auth_method == "2":
            return self.telegram_auth()
        else:
            print("Invalid authentication method")
            return None, None
    
    def get_telegram_users(self):
        """
        auth_type이 'telegram'인 모든 사용자의 정보를 조회합니다.
        
        Returns:
            list of tuples: 각 튜플은 (user_id, thread_id, telegram_id, first_name, last_name, username) 형식입니다.
        """
        query = """
        SELECT u.id, u.thread_id, t.telegram_id, t.first_name, t.last_name, t.username
        FROM users u
        JOIN auth_methods am ON u.id = am.user_id
        JOIN telegram_auth t ON am.id = t.auth_method_id
        WHERE am.auth_type = 'telegram'
        """
        
        try:
            cursor = self.conn.cursor()
            cursor.execute(query)
            results = cursor.fetchall()
            return results
        except sqlite3.Error as e:
            print(f"데이터베이스 쿼리 실행 중 오류 발생: {e}")
            return []
    
    def get_user_id_by_telegram_id(self, telegram_id):
        """
        telegram_id에 해당하는 user_id를 조회합니다.
        
        Args:
            telegram_id (str): 텔레그램 사용자 ID
        
        Returns:
            int or None: 해당하는 user_id, 없으면 None
        """
        query = """
        SELECT user_id
        FROM telegram_auth
        WHERE telegram_id = ?
        """
        
        try:
            cursor = self.conn.cursor()
            cursor.execute(query, (telegram_id,))
            result = cursor.fetchone()
            return result[0] if result else None
        except sqlite3.Error as e:
            print(f"데이터베이스 쿼리 실행 중 오류 발생: {e}")
            return None
    
    def set_conversation_times(self, user_id, times):
        c = self.conn.cursor()
        c.execute("DELETE FROM message_schedule WHERE user_id = ?", (user_id,))
        for t in times:
            c.execute("INSERT INTO message_schedule (user_id, schedule_time) VALUES (?, ?)", 
                        (user_id, t.strftime("%H:%M")))
        self.conn.commit()
        
    def get_message_times(self, user_id):
        c = self.conn.cursor()
        c.execute("SELECT schedule_time FROM message_schedule WHERE user_id = ?", (user_id,))
        return [datetime.strptime(row[0], "%H:%M").time() for row in c.fetchall()]
    
    def get_users_by_schedule_time(self):
        c = self.conn.cursor()
        c.execute("SELECT user_id, schedule_time FROM message_schedule")
        
        schedule_dict = {}
        for row in c.fetchall():
            user_id = row[0]
            schedule_time = datetime.strptime(row[1], "%H:%M").time()
            
            if schedule_time not in schedule_dict:
                schedule_dict[schedule_time] = []
            schedule_dict[schedule_time].append(user_id)
        
        return schedule_dict

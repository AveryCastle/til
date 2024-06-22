import sqlite3
from sqlite3 import Error

class DatabaseManager:
    def __init__(self, db_name='befriends.db'):
        self.conn = self.create_connection(db_name)
        self.create_tables()

    def create_connection(self, db_name):
        conn = None
        try:
            conn = sqlite3.connect(db_name)
            print(sqlite3.version)
        except Error as e:
            print(e)
        return conn

    def create_tables(self):
        try:
            # fren_users 테이블 생성
            sql_create_user_table = """ CREATE TABLE IF NOT EXISTS users (
                                            id integer PRIMARY KEY AUTOINCREMENT,
                                            thread_id text,
                                            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                                            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                                        ); """
            
            # users 인증 방법 테이블 생성
            sql_create_user_auth_table = """ 
                                            CREATE TABLE IF NOT EXISTS auth_methods (
                                                id integer PRIMARY KEY AUTOINCREMENT,
                                                user_id integer NOT NULL,
                                                auth_type text NOT NULL CHECK(auth_type IN ('telegram', 'kakaotalk', 'email')),
                                                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                                                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                                                FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
                                            );
                                        """
            # email_auth 테이블 생성
            sql_create_email_auth_table = """   CREATE TABLE IF NOT EXISTS email_auth (
                                                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                                                    auth_method_id INTEGER NOT NULL,
                                                    email_address TEXT NOT NULL,
                                                    password TEXT NOT NULL,
                                                    FOREIGN KEY (auth_method_id) REFERENCES auth_methods (id) ON DELETE CASCADE
                                                );
            """

            # email_auth 테이블 생성
            sql_create_telegram_auth_table = """ CREATE TABLE IF NOT EXISTS telegram_auth (
                                                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                                                    auth_method_id INTEGER NOT NULL,
                                                    telegram_id TEXT NOT NULL,
                                                    first_name TEXT,
                                                    last_name TEXT,
                                                    username TEXT,
                                                    FOREIGN KEY (auth_method_id) REFERENCES auth_methods (id) ON DELETE CASCADE
                                                );
            """
            
            # conversation 테이블 생성
            sql_create_conversation_table = """ CREATE TABLE IF NOT EXISTS conversation (
                                                    id integer PRIMARY KEY AUTOINCREMENT,
                                                    user_id integer NOT NULL UNIQUE,
                                                    messages text NOT NULL,
                                                    thread_id text,
                                                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                                                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                                                    FOREIGN KEY (user_id) REFERENCES fren_users (id)
                                                ); """
            
            c = self.conn.cursor()
            c.execute(sql_create_user_table)
            c.execute(sql_create_conversation_table)
        except Error as e:
            print(e)

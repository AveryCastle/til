import sqlite3
from sqlite3 import Error
import json

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
                                            email text NOT NULL UNIQUE,
                                            password text NOT NULL,
                                            thread_id text,
                                            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                                            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                                        ); """
            
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

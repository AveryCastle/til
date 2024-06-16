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
                                            thread_id text
                                        ); """
            
            # conversation 테이블 생성
            sql_create_conversation_table = """ CREATE TABLE IF NOT EXISTS conversation (
                                                    id integer PRIMARY KEY AUTOINCREMENT,
                                                    user_id integer NOT NULL,
                                                    messages text NOT NULL,
                                                    FOREIGN KEY (user_id) REFERENCES fren_users (id)
                                                ); """
            
            c = self.conn.cursor()
            c.execute(sql_create_user_table)
            c.execute(sql_create_conversation_table)
        except Error as e:
            print(e)

    def insert_conversation(self, user_id, messages):
        try:
            sql_insert_conversation = """INSERT INTO conversation (user_id, messages) VALUES (?, ?);"""
            c = self.conn.cursor()
            c.execute(sql_insert_conversation, (user_id, json.dumps(messages)))
            self.conn.commit()
        except Error as e:
            print(e)

    def get_conversations(self, user_id):
        try:
            sql_get_conversations = """SELECT messages FROM conversation WHERE user_id = ?;"""
            c = self.conn.cursor()
            c.execute(sql_get_conversations, (user_id,))
            rows = c.fetchall()
            return [json.loads(row[0]) for row in rows]
        except Error as e:
            print(e)
            return []

import sqlite3
from sqlite3 import Error

class DatabaseManager:
    def __init__(self, db_name='gpts.db'):
        self.conn = self.create_connection(db_name)
        self.create_table()

    def create_connection(self, db_name):
        conn = None
        try:
            conn = sqlite3.connect(db_name)
            print(sqlite3.version)
        except Error as e:
            print(e)
        return conn

    def create_table(self):
        try:
            sql_create_user_table = """ CREATE TABLE IF NOT EXISTS fren_users (
                                            id integer PRIMARY KEY,
                                            email text NOT NULL UNIQUE,
                                            password text NOT NULL,
                                            thread_id text
                                        ); """
            c = self.conn.cursor()
            c.execute(sql_create_user_table)
        except Error as e:
            print(e)

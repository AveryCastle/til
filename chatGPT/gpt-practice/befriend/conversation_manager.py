from sqlite3 import Error
import json

class ConversationManager:
    def __init__(self, db_manager):
        self.conn = db_manager.conn

    def upsert_conversation(self, user_id, messages, thread_id):
        print("upsert_conversation", user_id, messages, thread_id) 
        try:
            sql_upsert_conversation = """INSERT INTO conversation (user_id, messages, thread_id)
                                VALUES (?, ?, ?)
                                ON CONFLICT(user_id) DO UPDATE SET
                                messages=excluded.messages,
                                thread_id=excluded.thread_id;"""
            c = self.conn.cursor()
            c.execute(sql_upsert_conversation, (user_id, json.dumps(messages, ensure_ascii=False), thread_id))
            self.conn.commit()
        except Error as e:
            print(e)

    def get_conversations(self, user_id):
        try:
            sql_get_conversations = """SELECT messages FROM conversation WHERE user_id = ?;"""
            c = self.conn.cursor()
            c.execute(sql_get_conversations, (user_id,))
            rows = c.fetchall()
            
            if not rows:
                # 데이터가 없을 때 기본 메시지 반환
                return [{'role': 'user', 'message': '안녕?'}], None
            
            return [json.loads(row[0]) for row in rows], rows[0][1]
        except Error as e:
            print(e)
            return []

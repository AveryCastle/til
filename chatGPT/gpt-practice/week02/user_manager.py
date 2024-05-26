import hashlib

class UserManager:
    def __init__(self, db_manager):
        self.conn = db_manager.conn

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def get_user_count(self):
        c = self.conn.cursor()
        c.execute("SELECT COUNT(*) FROM fren_users")
        count = c.fetchone()[0]
        return count

    def check_user(self, email, password):
        c = self.conn.cursor()
        c.execute("SELECT * FROM fren_users WHERE email=?", (email,))
        rows = c.fetchall()

        if rows:
            stored_password = rows[0][2]
            if stored_password == self.hash_password(password):
                return rows[0][0], rows[0][3]  # Return id and thread_id
            else:
                return "Incorrect password"
        else:
            return None

    def create_user(self, email, password):
        c = self.conn.cursor()
        id = self.get_user_count() + 1
        hashed_password = self.hash_password(password)
        c.execute("INSERT INTO fren_users(id, email, password) VALUES(?, ?, ?)", (id, email, hashed_password))
        self.conn.commit()
        return id

    def update_thread_id(self, user_id, thread_id):
        c = self.conn.cursor()
        c.execute("UPDATE fren_users SET thread_id=? WHERE id=?", (thread_id, user_id))
        self.conn.commit()

    def user_input(self):
        email = input("Enter email: ")
        password = input("Enter password: ")

        user_check = self.check_user(email, password)
        if user_check is None:
            id = self.create_user(email, password)
            print("New user created. User id: ", id)
            return id, None
        elif user_check == "Incorrect password":
            print(user_check)
            return None, None
        else:
            print("Existing user. User id and thread_id: ", user_check)
            return user_check

import sqlite3
from hashlib import sha256
from datetime import datetime, timedelta

class DataBaseManager:
    def __init__(self, db_name='chat_system.db'):
        self.conn = sqlite3.connect(db_name, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.create_tables()
    
    def create_tables(self):

        #Tabel pentru utilizatori
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        ''')

        #Tabel pentru grupuri
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS groups (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                access_code TEXT NOT NULL,
                admin_id INTEGER,
                FOREIGN KEY (admin_id) REFERENCES users (id)
            )
        ''')

        #Tabel pentru mesaje
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sender_id INTEGER,
                receiver_id INTEGER,
                content TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                is_group BOOLEAN,
                expires_at DATETIME,
                FOREIGN KEY (sender_id) REFERENCES users (id)
            )
        ''')

        #Tabel pentru membri grup
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS group_members (
                user_id INTEGER,
                group_id INTEGER,
                joined_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (user_id, group_id),
                FOREIGN KEY (user_id) REFERENCES users (id),
                FOREIGN KEY (group_id) REFERENCES groups (id)
            )   
        ''')

        self.conn.commit()
    
    def hash_password(self, password):
        return sha256(password.encode()).hexdigest()
    
    def add_user(self, username, password):
        try:
            hashed_password = self.hash_password(password)
            self.cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False # Utilizatorul exista deja
        
    def verify_user(self, username, password):
        hashed_password = self.hash_password(password)
        self.cursor.execute("SELECT id FROM users WHERE username = ? AND password = ?", (username, hashed_password))
        result = self.cursor.fetchone()
        return result[0] if result else None

    def save_message(self, sender_id, receiver_id, content, is_group=False, expiry_minutes=None):
        expires_at = None
        if expiry_minutes:
            expires_at = datetime.now() + timedelta(minutes=expiry_minutes)
        
        self.cursor.execute('''
            INSERT INTO messages (sender_id, receiver_id, content, is_group, expires_at)
            VALUES (?, ?, ?, ?, ?)
        ''', (sender_id, receiver_id, content, is_group, expires_at))
        self.conn.commit()          

    def delete_expired_messages(self):
        self.cursor.execute("DELETE FROM messages WHERE expires_at IS NOT NULL AND expires_at < ?", (datetime.now(),))
        self.conn.commit()
    
    def join_group(self, user_id, group_name, provided_code):
        self.cursor.execute("SELECT id FROM groups WHERE name = ? AND access_code = ?", (group_name, provided_code))
        group = self.cursor.fetchone()

        if group:
            group_id = group[0]
            return self.add_user_to_group(user_id, group_id)
        return False # Cod gresit sau grup inexistent
    
    def add_user_to_group(self, user_id, group_id):
        try:
            self.cursor.execute("INSERT INTO group_members (user_id, group_id) VALUES (?, ?)", (user_id, group_id))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return True # Utilizatorul este deja membru al grupului
        
    def get_chat_history(self, user_id, peer_id, is_group=False):
        if is_group:
            query = "SELECT sender_id, content, timestamp FROM messages WHERE receiver_id = ? AND is_group = 1 ORDER BY timestamp ASC"
            params = (peer_id,)
        else:
            query = """
                SELECT sender_id, content, timestamp FROM messages 
                WHERE (sender_id = ? AND receiver_id = ? AND is_group = 0) 
                OR (sender_id = ? AND receiver_id = ? AND is_group = 0)
                ORDER BY timestamp ASC
            """
            params = (user_id, peer_id, peer_id, user_id) 
        self.cursor.execute(query, params)
        return self.cursor.fetchall()
    
    def get_all_users(self, exclude_id):
        self.cursor.execute("SELECT id, username FROM users WHERE id != ?", (exclude_id,))
        return self.cursor.fetchall()
        





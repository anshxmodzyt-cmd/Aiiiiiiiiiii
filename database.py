import sqlite3

def init_db():
    conn = sqlite3.connect('platform.db', check_same_thread=False)
    cursor = conn.cursor()
    
    # Users Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            plan TEXT DEFAULT 'Free',
            daily_limit INTEGER DEFAULT 20,
            used_today INTEGER DEFAULT 0,
            is_admin INTEGER DEFAULT 0
        )
    ''')
    
    # System Settings Table (Controlled by Admin Panel)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS settings (
            key TEXT PRIMARY KEY,
            value TEXT
        )
    ''')
    
    # Default Admin User & Settings Insert
    cursor.execute("INSERT OR IGNORE INTO users (id, username, email, password, plan, daily_limit, is_admin) VALUES (1, 'ansh', 'admin@anshai.com', 'admin123', 'VIP', 99999, 1)")
    cursor.execute("INSERT OR IGNORE INTO users (id, username, email, password, plan, daily_limit, is_admin) VALUES (2, 'coder_user', 'user@gmail.com', 'user123', 'Free', 20, 0)")
    cursor.execute("INSERT OR IGNORE INTO settings (key, value) VALUES ('ai_name', 'Ansh-AI')")
    cursor.execute("INSERT OR IGNORE INTO settings (key, value) VALUES ('system_prompt', 'You are Ansh-AI, an expert software developer and assistant created by Ansh.')")
    
    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
    print("Database Initialized Successfully!")

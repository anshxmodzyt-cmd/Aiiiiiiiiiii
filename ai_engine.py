import sqlite3

class CustomAIEngine:
    def __init__(self):
        print("Initializing Cloud AI Engine...")

    def get_system_settings(self):
        conn = sqlite3.connect('platform.db', check_same_thread=False)
        cursor = conn.cursor()
        cursor.execute("SELECT key, value FROM settings")
        settings = dict(cursor.fetchall())
        conn.close()
        return settings

    def generate_response(self, user_prompt: str) -> str:
        settings = self.get_system_settings()
        ai_name = settings.get('ai_name', 'Ansh-AI')
        
        return f"[{ai_name} Cloud Engine Response]\n\nAapka sawaal: '{user_prompt}'\n\nYeh lijiye aapka solution:\n```python\n# Clean Code Output\ndef solve():\n    print('Hello! Your custom AI platform is working perfectly.')\n\nsolve()\n```"

ai_engine = CustomAIEngine()

import sqlite3
import requests

class CustomAIEngine:
    def __init__(self):
        print("Initializing Local Ollama AI Engine...")

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
        system_prompt = settings.get('system_prompt', 'You are an expert software developer and assistant.')

        # Combining system instructions with user prompt for the local model
        full_prompt = f"System Instruction: {system_prompt}\n\nUser Query: {user_prompt}"

        try:
            # Connecting to Local Ollama Server (Make sure Ollama is running on your PC)
            response = requests.post("http://localhost:11434/api/generate", json={
                "model": "llama3",  # Aap yahan deepseek-r1 ya koi aur model bhi daal sakte hain jo aapne install kiya ho
                "prompt": full_prompt,
                "stream": False
            }, timeout=60)

            if response.status_code == 200:
                return response.json().get("response", "AI response generation failed.")
            else:
                return f"⚠️ Local AI Server Error: Status code {response.status_code}"
                
        except requests.exceptions.ConnectionError:
            return "⚠️ Ollama Local Server connected nahi hai! Pehle terminal mein `ollama run llama3` start karein."
        except Exception as e:
            return f"⚠️ Error: {str(e)}"

ai_engine = CustomAIEngine()

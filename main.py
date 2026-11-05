from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import sqlite3
from ai_engine import ai_engine
from database import init_db

app = FastAPI(title="Ansh-AI Custom Platform")
templates = Jinja2Templates(directory="templates")

# Initialize DB on startup
init_db()

class ChatRequest(BaseModel):
    user_id: int
    message: str

class PlanUpdate(BaseModel):
    user_id: int
    new_plan: str
    new_limit: int

@app.get("/", response_class=HTMLResponse)
def user_chat_page(request: Request):
    return templates.TemplateResponse(request, "index.html", {})

@app.get("/admin", response_class=HTMLResponse)
def admin_dashboard(request: Request):
    conn = sqlite3.connect('platform.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, email, plan, daily_limit, used_today, is_admin FROM users")
    users = cursor.fetchall()
    
    cursor.execute("SELECT key, value FROM settings")
    settings = dict(cursor.fetchall())
    conn.close()
    
    return templates.TemplateResponse(request, "admin.html", {
        "users": users,
        "settings": settings
    })

@app.post("/api/chat")
def chat_endpoint(data: ChatRequest):
    conn = sqlite3.connect('platform.db')
    cursor = conn.cursor()
    
    # 1. Check User & Quota Limits
    cursor.execute("SELECT daily_limit, used_today, plan FROM users WHERE id=?", (data.user_id,))
    user = cursor.fetchone()
    
    if not user:
        conn.close()
        raise HTTPException(status_code=404, detail="User not found")
        
    daily_limit, used_today, plan = user
    
    if daily_limit < 99999 and used_today >= daily_limit:
        conn.close()
        return {
            "status": "limit_reached", 
            "reply": "⚠️ Aapki aaj ki daily message limit khatam ho gayi hai!"
        }
    
    # 2. Generate AI Response
    reply = ai_engine.generate_response(data.message)
    
    # 3. Increment Usage Counter
    cursor.execute("UPDATE users SET used_today = used_today + 1 WHERE id=?", (data.user_id,))
    conn.commit()
    conn.close()
    
    return {
        "status": "success", 
        "reply": reply, 
        "used_today": used_today + 1, 
        "daily_limit": daily_limit
    }

@app.post("/api/admin/update-plan")
def update_user_plan(data: PlanUpdate):
    conn = sqlite3.connect('platform.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET plan=?, daily_limit=? WHERE id=?", (data.new_plan, data.new_limit, data.user_id))
    conn.commit()
    conn.close()
    return {"status": "success", "message": "User plan updated successfully!"}

from fastapi import FastAPI, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
import uvicorn
app = FastAPI(title="Auth Service")

# Allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

users_db = {"admin": "1234", "test": "abcd"}

@app.post("/login")
def login(username: str = Form(...), password: str = Form(...)):
    if username in users_db and users_db[username] == password:
        return {"message": "Login success", "status": "ok"}
    raise HTTPException(status_code=401, detail="Invalid credentials")

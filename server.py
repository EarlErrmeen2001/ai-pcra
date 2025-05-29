from fastapi import FastAPI, Request
from github import Github
import subprocess

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "API is running."}

@app.post("/webhook")
async def handle_webhook(request: Request):
    payload = await request.json()
    if payload.get("action") == "opened":
        pr_url = payload["pull_request"]["diff_url"]
        subprocess.run(["python", "ai_reviewer.py", pr_url])
    return {"status": "ok"}

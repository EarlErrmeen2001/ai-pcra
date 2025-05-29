from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from github import Github
import subprocess
import os

app = FastAPI()

# Serve React static files
app.mount("/static", StaticFiles(directory="static/static"), name="static")

@app.get("/")
async def serve_index():
    return FileResponse("static/index.html")


@app.get("/{full_path:path}")
async def serve_react_app(full_path: str):
    """Serve React frontend for all unrecognized routes (client-side routing)"""
    file_path = f"static/{full_path}"
    if os.path.exists(file_path):
        return FileResponse(file_path)
    return FileResponse("static/index.html")


@app.post("/webhook")
async def handle_webhook(request: Request):
    payload = await request.json()
    if payload.get("action") == "opened":
        pr_url = payload["pull_request"]["diff_url"]
        subprocess.run(["python", "reviewer_of_ai.py", pr_url])
    return {"status": "ok"}

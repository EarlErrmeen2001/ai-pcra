from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import os
import json

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# === Mount React frontend ===
app.mount("/static", StaticFiles(directory="app/static/static"), name="static")

@app.get("/")
def serve_index():
    return FileResponse("app/static/index.html")

@app.get("/favicon.ico")
def serve_favicon():
    return FileResponse("app/static/favicon.ico")

@app.get("/manifest.json")
def serve_manifest():
    return FileResponse("app/static/manifest.json")

@app.get("/logo192.png")
def serve_logo192():
    return FileResponse("app/static/logo192.png")

@app.get("/logo512.png")
def serve_logo512():
    return FileResponse("app/static/logo512.png")

@app.get("/{full_path:path}")
async def serve_spa(full_path: str):
    return FileResponse("app/static/index.html")

# === Review history logic ===
HISTORY_FILE = "app/review_history.json"

if not os.path.exists(HISTORY_FILE):
    with open(HISTORY_FILE, "w") as f:
        json.dump([], f)

def load_reviews():
    with open(HISTORY_FILE, "r") as f:
        return json.load(f)

def save_review(filename, issues):
    reviews = load_reviews()
    reviews.insert(0, {"filename": filename, "issues": issues})
    with open(HISTORY_FILE, "w") as f:
        json.dump(reviews, f)

@app.post("/webhook")
async def webhook(request: Request):
    data = await request.json()
    filename = data.get("filename")
    code = data.get("code")

    issues = []
    for i, line in enumerate(code.split("\n"), 1):
        if "print(" in line:
            issues.append({"line": i, "issue": "Avoid using print statements in production."})
        if "== None" in line:
            issues.append({"line": i, "issue": "Use 'is' when comparing to None."})

    save_review(filename, issues)
    return JSONResponse(content={"status": "received", "issues": issues})

@app.get("/api/reviews")
def get_reviews():
    return load_reviews()

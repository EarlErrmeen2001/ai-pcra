from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import os
import json

app = FastAPI()

# Allow CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static React files
app.mount("/static", StaticFiles(directory="app/static/static"), name="static")

# ✅ FIRST: Define /api route
@app.get("/api/reviews")
async def get_reviews():
    try:
        with open("app/data.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

# ✅ THEN: Define POST /webhook
@app.post("/webhook")
async def webhook(request: Request):
    data = await request.json()
    filename = data.get("filename")
    code = data.get("code")

    issues = []
    lines = code.split("\n")
    for i, line in enumerate(lines, start=1):
        if "print(" in line:
            issues.append({"line": i, "issue": "Avoid using print statements in production."})
        if "== None" in line:
            issues.append({"line": i, "issue": "Use 'is' when comparing to None."})

    with open("app/data.json", "w") as f:
        json.dump([{"filename": filename, "issues": issues}], f)

    return JSONResponse(content={"status": "received", "issues": issues})

# ✅ Then: index.html at root
@app.get("/")
async def serve_root():
    return FileResponse("app/static/index.html")

# ✅ LAST: Wildcard route for React Router
@app.get("/{full_path:path}")
async def serve_react_app(full_path: str):
    index_path = os.path.join("app", "static", "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return JSONResponse(status_code=404, content={"detail": "Not Found"})

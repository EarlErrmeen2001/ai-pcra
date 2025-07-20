from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI()

# CORS for frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files (React build)
app.mount("/static", StaticFiles(directory="app/static/static"), name="static")

# Serve index.html at root
@app.get("/")
async def serve_root():
    return FileResponse("app/static/index.html")

# Handle unmatched frontend routes (for React Router)
@app.get("/{full_path:path}")
async def serve_react_app(full_path: str):
    index_path = os.path.join("app", "static", "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return JSONResponse(status_code=404, content={"detail": "Not Found"})

# Webhook POST endpoint
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

    # Save latest webhook submission (simulate DB)
    with open("app/data.json", "w") as f:
        import json
        json.dump([{"filename": filename, "issues": issues}], f)

    return JSONResponse(content={"status": "received", "issues": issues})

# API to retrieve latest webhook review results
@app.get("/api/reviews")
async def get_reviews():
    try:
        with open("app/data.json", "r") as f:
            import json
            return json.load(f)
    except FileNotFoundError:
        return []

from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI()

# CORS (helpful for development or cross-origin frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Use specific origins in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve the React static build
app.mount("/static", StaticFiles(directory="app/static/static"), name="static")

# Serve index.html at root
@app.get("/")
async def serve_index():
    return FileResponse("app/static/index.html")

# Catch-all to support React Router
@app.get("/{full_path:path}")
async def serve_react_app(full_path: str):
    file_path = os.path.join("app", "static", full_path)
    if os.path.exists(file_path) and not os.path.isdir(file_path):
        return FileResponse(file_path)
    return FileResponse("app/static/index.html")

# In-memory storage for demo purposes
review_results = []

@app.post("/webhook")
async def handle_webhook(payload: dict):
    code = payload.get("code", "")
    issues = []

    # Simple static checks
    if "print(" in code:
        issues.append({"line": 1, "issue": "Avoid using print statements in production."})
    if "==" in code and "None" in code:
        issues.append({"line": 2, "issue": "Use 'is' when comparing to None."})

    review_results.append({
        "filename": payload.get("filename", "unnamed"),
        "issues": issues
    })

    return {"status": "received", "issues": issues}

@app.get("/api/reviews")
async def get_reviews():
    return review_results

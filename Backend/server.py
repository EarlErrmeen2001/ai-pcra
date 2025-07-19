from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import os

app = FastAPI()

# Enable CORS (allow all origins for now)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ In-memory storage for webhook-submitted reviews
submitted_reviews: List[dict] = []

# ✅ Mount the React frontend from app/static
app.mount("/", StaticFiles(directory="app/static", html=True), name="static")

# ✅ Return all submitted review results
@app.get("/api/reviews")
def get_reviews():
    return submitted_reviews

# ✅ Webhook handler to analyze code and store the result
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

    # Store for frontend access
    submitted_reviews.append({
        "filename": filename,
        "issues": len(issues),
        "details": issues
    })

    return JSONResponse(content={"status": "received", "issues": issues})

# ✅ Fallback to serve React index.html for unknown routes
@app.get("/{full_path:path}")
async def serve_react_app(full_path: str):
    index_path = os.path.join("app", "static", "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return JSONResponse(status_code=404, content={"detail": "Not Found"})

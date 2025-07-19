from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI()

# Enable CORS (optional but useful)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ API route first
@app.get("/api/reviews")
def get_reviews():
    return [
        {"filename": "file1.py", "issues": 5},
        {"filename": "file2.py", "issues": 2}
    ]

# ✅ Webhook POST handler
@app.post("/webhook")
async def webhook(request: Request):
    data = await request.json()
    filename = data.get("filename")
    code = data.get("code")

    issues = []
    for i, line in enumerate(code.splitlines(), start=1):
        if "print(" in line:
            issues.append({"line": i, "issue": "Avoid using print statements in production."})
        if "== None" in line:
            issues.append({"line": i, "issue": "Use 'is' when comparing to None."})

    return JSONResponse(content={"status": "received", "issues": issues})

# ✅ Catch-all route for React Router (must come before mount)
@app.get("/{full_path:path}")
async def serve_react_app(full_path: str):
    index_path = os.path.join("app", "static", "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return JSONResponse(status_code=404, content={"detail": "Not Found"})

# ✅ Finally mount the React app at root AFTER all routes are declared
app.mount("/", StaticFiles(directory="app/static", html=True), name="static")

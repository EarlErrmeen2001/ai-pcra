from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI()

# CORS settings (adjust in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ API route: reviews
@app.get("/api/reviews")
def get_reviews():
    return [
        {"filename": "file1.py", "issues": 5},
        {"filename": "file2.py", "issues": 2}
    ]

# ✅ API route: webhook POST
@app.post("/webhook")
async def webhook(request: Request):
    data = await request.json()
    filename = data.get("filename")
    code = data.get("code")

    issues = []
    for i, line in enumerate(code.split("\n"), start=1):
        if "print(" in line:
            issues.append({"line": i, "issue": "Avoid using print statements in production."})
        if "== None" in line:
            issues.append({"line": i, "issue": "Use 'is' when comparing to None."})
    return JSONResponse(content={"status": "received", "issues": issues})

# ✅ Mount static React build BEFORE wildcard route
app.mount("/static", StaticFiles(directory="app/static/static"), name="static")
app.mount("/", StaticFiles(directory="app/static", html=True), name="frontend")

# ✅ Catch-all route for React Router (after static + API)
@app.get("/{full_path:path}")
async def serve_react_app(full_path: str):
    index_path = os.path.join("app", "static", "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return JSONResponse(status_code=404, content={"detail": "Not Found"})

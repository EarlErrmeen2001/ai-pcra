from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI()

# CORS (optional)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static React build
app.mount("/static", StaticFiles(directory="app/static/static"), name="static")

@app.get("/favicon.ico")
async def favicon():
    return FileResponse("app/static/favicon.ico")

@app.get("/manifest.json")
async def manifest():
    return FileResponse("app/static/manifest.json")

@app.get("/api/reviews")
def get_reviews():
    return [
        {"filename": "file1.py", "issues": 5},
        {"filename": "file2.py", "issues": 2}
    ]

# Catch-all: Serve index.html for frontend routes
@app.get("/{full_path:path}")
async def serve_react_app(request: Request, full_path: str):
    index_path = os.path.join("app", "static", "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"detail": "Not Found"}

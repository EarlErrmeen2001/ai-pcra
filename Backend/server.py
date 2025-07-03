from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import os

app = FastAPI()

# Serve React static files
app.mount("/static", StaticFiles(directory="app/static/static"), name="static")

# API sample route (you can add more)
@app.get("/api/health")
def health_check():
    return {"status": "ok"}

# Serve the React frontend
@app.get("/")
@app.get("/{full_path:path}")
def serve_react_app(full_path: str = ""):
    index_file_path = os.path.join("app/static", "index.html")
    return FileResponse(index_file_path)

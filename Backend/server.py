from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
import os

app = FastAPI()

# Serve React build (static files)
static_dir = Path(__file__).parent / "app" / "static"
app.mount("/static", StaticFiles(directory=static_dir / "static"), name="static")

@app.get("/", include_in_schema=False)
async def serve_react_index():
    index_path = static_dir / "index.html"
    if index_path.exists():
        return FileResponse(index_path)
    return {"detail": "index.html not found"}

@app.get("/{full_path:path}", include_in_schema=False)
async def serve_react_app(full_path: str):
    """
    Serve React frontend for any path not matched by backend
    """
    index_path = static_dir / "index.html"
    if index_path.exists():
        return FileResponse(index_path)
    return {"detail": "Page not found"}

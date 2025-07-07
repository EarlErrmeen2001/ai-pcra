from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path

app = FastAPI()

# Serve React static files
app.mount("/static", StaticFiles(directory="app/static/static"), name="static")

@app.get("/")
def serve_index():
    return FileResponse("app/static/index.html")

@app.get("/{full_path:path}")
def serve_react_app(full_path: str):
    index_path = Path("app/static/index.html")
    if index_path.exists():
        return FileResponse(index_path)
    return {"detail": "Page not found"}

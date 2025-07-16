from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

app = FastAPI()

# Serve subdirectory static files
app.mount("/static", StaticFiles(directory="app/static/static"), name="static")

@app.get("/api/health")
def health_check():
    return {"status": "ok"}

# Serve root-level frontend files
@app.get("/")
def serve_index():
    return FileResponse("app/static/index.html")

@app.get("/favicon.ico")
def serve_favicon():
    return FileResponse("app/static/favicon.ico")

@app.get("/manifest.json")
def serve_manifest():
    return FileResponse("app/static/manifest.json")

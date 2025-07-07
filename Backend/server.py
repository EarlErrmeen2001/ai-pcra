from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

app = FastAPI()

# Serve static React files
app.mount("/static", StaticFiles(directory="app/static/static"), name="static")

# API route example (replace with yours)
@app.get("/api/health")
def health_check():
    return {"status": "ok"}

# Root route to serve React app
@app.get("/")
def read_index():
    return FileResponse("app/static/index.html")

from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import os

app = FastAPI()

# Serve React static files
app.mount("/static", StaticFiles(directory="app/static/static"), name="static")

@app.get("/api/analyze")
async def analyze():
    # Placeholder logic for actual analysis
    return {"message": "Analysis complete!"}

# Catch-all route to serve index.html (React frontend)
@app.get("/{full_path:path}")
async def serve_react_app(request: Request, full_path: str):
    index_file_path = os.path.join("app", "static", "index.html")
    if os.path.exists(index_file_path):
        return FileResponse(index_file_path)
    return JSONResponse(status_code=404, content={"detail": "Frontend not found"})

# For local development (optional)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:app", host="0.0.0.0", port=8000)

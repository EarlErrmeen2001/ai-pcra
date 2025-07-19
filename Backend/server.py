from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI()

# Allow cross-origin requests if needed
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can restrict this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount React build folder
app.mount("/", StaticFiles(directory="app/static", html=True), name="static")


# Example API endpoint
@app.get("/api/reviews")
def get_reviews():
    return [
        {"filename": "file1.py", "issues": 5},
        {"filename": "file2.py", "issues": 2}
    ]


# Serve index.html for all unmatched routes (supports React Router)
@app.get("/{full_path:path}")
async def serve_react_app(full_path: str):
    index_path = os.path.join("app", "static", "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"detail": "Not Found"}

# 🚀 Capital City University TEAM 👨‍💻👩‍💻🧠💻
# ===================================
# 🔬 Capital City University AI-Powered Code Review Assistant
# 🧑‍💻 Lead Dev: Alameen Idris Muhammad
# 👥 Team: Collaborating to catch bugs 🐛,
#          review Python code 🐍, and
#          deploy with confidence 🎯
# -----------------------------------
# 💻 React + FastAPI + SQLite
# 📦 Deployed on Render
# 🌍 Smart automation for better code!
from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import Column, Integer, String, create_engine, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
import json

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database setup
DATABASE_URL = "sqlite:///./reviews.db"
Base = declarative_base()
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)
session = SessionLocal()

class Review(Base):
    __tablename__ = "reviews"
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    issues = Column(Text)  # Stored as JSON string

Base.metadata.create_all(bind=engine)

# Serve frontend
app.mount("/static", StaticFiles(directory="app/static/static"), name="static")

@app.get("/")
async def serve_index():
    return FileResponse("app/static/index.html")

@app.get("/favicon.ico")
async def favicon():
    return FileResponse("app/static/favicon.ico")

@app.post("/webhook")
async def webhook(request: Request):
    data = await request.json()
    filename = data.get("filename")
    code = data.get("code")

    issues = []
    lines = code.split("\n")
    for i, line in enumerate(lines, start=1):
        if "print(" in line:
            issues.append({"line": i, "issue": "Avoid using print statements in production."})
        if "== None" in line:
            issues.append({"line": i, "issue": "Use 'is' when comparing to None."})

    review = Review(filename=filename, issues=json.dumps(issues))
    session.add(review)
    session.commit()

    return JSONResponse(content={"status": "received", "issues": issues})

@app.get("/api/reviews")
def get_reviews():
    reviews = session.query(Review).all()
    return [
        {
            "filename": r.filename,
            "issues": json.loads(r.issues)
        }
        for r in reviews
    ]

# Catch-all for React Router paths (must be last)
@app.get("/{full_path:path}")
async def serve_react_app(full_path: str):
    return FileResponse("app/static/index.html")

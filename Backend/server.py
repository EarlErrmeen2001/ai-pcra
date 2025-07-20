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

# Allow all CORS origins (adjust in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Setup SQLite DB
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

# Serve React build
app.mount("/", StaticFiles(directory="app/static", html=True), name="static")

# 📨 Webhook handler
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

    # Save to database
    review = Review(filename=filename, issues=json.dumps(issues))
    session.add(review)
    session.commit()

    return JSONResponse(content={"status": "received", "issues": issues})

# 🧾 Get stored reviews
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

# React route fallback
@app.get("/{full_path:path}")
async def serve_react_app(full_path: str):
    index_path = os.path.join("app", "static", "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return JSONResponse(status_code=404, content={"detail": "Not Found"})

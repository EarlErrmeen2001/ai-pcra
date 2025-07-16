from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List
import os

app = FastAPI()

# In-memory store
reviews_db = []

class CodeReviewRequest(BaseModel):
    filename: str
    code: str

class Issue(BaseModel):
    line: int
    issue: str

@app.post("/webhook")
async def handle_webhook(data: CodeReviewRequest):
    code = data.code
    filename = data.filename
    issues: List[Issue] = []

    lines = code.splitlines()
    for idx, line in enumerate(lines, start=1):
        if "print(" in line:
            issues.append(Issue(line=idx, issue="Avoid using print statements in production."))
        if "== None" in line:
            issues.append(Issue(line=idx, issue="Use 'is' when comparing to None."))

    reviews_db.append({
        "filename": filename,
        "issues": issues
    })

    return {"status": "received", "issues": issues}

@app.get("/api/reviews")
async def get_reviews():
    return reviews_db
from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List
import os

app = FastAPI()

# In-memory store
reviews_db = []

class CodeReviewRequest(BaseModel):
    filename: str
    code: str

class Issue(BaseModel):
    line: int
    issue: str

@app.post("/webhook")
async def handle_webhook(data: CodeReviewRequest):
    code = data.code
    filename = data.filename
    issues: List[Issue] = []

    lines = code.splitlines()
    for idx, line in enumerate(lines, start=1):
        if "print(" in line:
            issues.append(Issue(line=idx, issue="Avoid using print statements in production."))
        if "== None" in line:
            issues.append(Issue(line=idx, issue="Use 'is' when comparing to None."))

    reviews_db.append({
        "filename": filename,
        "issues": issues
    })

    return {"status": "received", "issues": issues}

@app.get("/api/reviews")
async def get_reviews():
    return reviews_db

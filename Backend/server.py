from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/", StaticFiles(directory="app/static", html=True), name="static")


# ✅ ADD THIS MODEL FOR WEBHOOK INPUT
class CodePayload(BaseModel):
    filename: str
    code: str

# ✅ ADD THIS POST HANDLER
@app.post("/webhook")
async def webhook(payload: CodePayload):
    filename = payload.filename
    code = payload.code

    # Dummy analysis logic for now (you can improve it later)
    issues = []
    lines = code.splitlines()
    for idx, line in enumerate(lines, start=1):
        if "print(" in line:
            issues.append({"line": idx, "issue": "Avoid using print statements in production."})
        if "== None" in line:
            issues.append({"line": idx, "issue": "Use 'is' when comparing to None."})

    return {"status": "received", "issues": issues}

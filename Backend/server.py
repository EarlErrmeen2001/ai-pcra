from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

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
    
    return JSONResponse(content={"status": "received", "issues": issues})

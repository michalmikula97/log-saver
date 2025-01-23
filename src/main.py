import os
from pydantic import BaseModel
from fastapi import FastAPI, Form
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from starlette.requests import Request
from datetime import datetime

class LogMessage(BaseModel):
    message: str

app = FastAPI()

CURRENT_DIR = os.path.dirname(__file__)
LOG_DIR = CURRENT_DIR + "/data"
LOG_FILE = os.path.join(LOG_DIR, "logs.txt")

templates = Jinja2Templates(directory=CURRENT_DIR + "/templates")
app.mount("/static", StaticFiles(directory=CURRENT_DIR + "/static",html=True), name="static")

@app.get("/", response_class=JSONResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/log")
async def log_text(text: str = Form(...)):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"{timestamp} - {text}\n"
    
    with open(LOG_FILE, "a") as f:
        f.write(log_entry)
    return {"message": "Text logged successfully!"}

@app.get("/logs")
async def get_logs():
    if not os.path.exists(LOG_FILE) or os.stat(LOG_FILE).st_size == 0:
        return JSONResponse(content={"logs": "No logs yet."})

    with open(LOG_FILE, "r") as f:
        logs = f.read()
    return JSONResponse(content={"logs": logs})

@app.get("/ping")
async def get_pong():
    return {"message": "pong"}

@app.get("/error")
async def trigger_error():
    # This will raise an exception, effectively "crashing" the app
    os._exit(1)
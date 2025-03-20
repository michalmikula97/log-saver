import os
from pydantic import BaseModel
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from starlette.requests import Request
from db.database import Database
from fastapi.responses import Response


class LogMessage(BaseModel):
    message: str

class Book(BaseModel):
    title: str
    author: str

app = FastAPI()

db = Database()

CURRENT_DIR = os.path.dirname(__file__)
LOG_DIR = CURRENT_DIR + "/data"
LOG_FILE = os.path.join(LOG_DIR, "logs.txt")

templates = Jinja2Templates(directory=CURRENT_DIR + "/templates")
app.mount("/static", StaticFiles(directory=CURRENT_DIR + "/static",html=True), name="static")

@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return Response(status_code=204)  # No Content

@app.get("/", response_class=JSONResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/add-book")
async def add_book(book: Book):

    db.insert_book(book.title, book.author)

    return {"message": "Book added successfully!"}

@app.get("/logs")
async def get_logs():
    if not os.path.exists(LOG_FILE) or os.stat(LOG_FILE).st_size == 0:
        return JSONResponse(content={"logs": "No logs were stored yet."})

    with open(LOG_FILE, "r") as f:
        logs = f.read()
    return JSONResponse(content={"logs": logs})

@app.get("/books")
async def get_books():
    books = db.get_books()
    if not books:
        return {"books": "No books found."}
    formatted_books = "\n".join([f"{book['title']} - {book['author']}" for book in books])
    return {"books": formatted_books}

@app.get("/ping")
async def get_pong():
    return {"message": "pong"}

@app.get("/error")
async def trigger_error():
    # This will raise an exception, effectively "crashing" the app
    os._exit(1)
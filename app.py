from fastapi import FastAPI, HTTPException, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import Annotated
from models import ShortURL, save_url
import sqlite3

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Database connection
conn = sqlite3.connect('shorturls.db')
cursor = conn.cursor()

# Create table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS shorturls (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        code TEXT UNIQUE,
        url TEXT
    )
''')
conn.commit()


class ShortURL(BaseModel):
    url: str



@app.get("/")
async def root():
    return {"message": "Hi, please note that this endpoint is nothing but a  "}

@app.post("/shorten_url")
def shorten_url(url: ShortURL):

    code = save_url(url)
    return {"short_url": f"https://short.carlosbueno.xyz/{code}"}

@app.post("/create_short_url")
def create_short_url(url: Annotated[str, Form()]):
    print(url)

    return {"short_url": url}


@app.get("/create_short_url")
def create_short_url_form(request: Request):
    """Return an HTML form to create a new short URL."""
    return templates.TemplateResponse("create_short_url.html", {"request": request})


@app.get("/{short_code}")
def redirect_url(short_code: str):
    """Redirect to the original URL for the given short code."""
    conn = sqlite3.connect('shorturls.db')
    cursor = conn.cursor()

    cursor.execute("SELECT url FROM shorturls WHERE code=?", (short_code,))
    result = cursor.fetchone()

    cursor.close()
    conn.close()

    if result:
        redirect_url = 'https://' + result[0]
        return RedirectResponse(url=redirect_url)
    raise HTTPException(status_code=404, detail="Short URL not found.")

@app.get("/create_short_url", response_class=HTMLResponse)
def create_short_url_form(request: Request):
    """Return an HTML form to create a new short URL."""
    return templates.TemplateResponse("create_short_url.html", {"request": request})


from pydantic import BaseModel
import sqlite3
import string
import random

class ShortURL(BaseModel):
    url: str


def generate_short_code():
    """Generate a random alphanumeric code for the short URL."""
    characters = string.ascii_letters + string.digits
    code = ''.join(random.choice(characters) for _ in range(6))

    conn = sqlite3.connect('shorturls.db')
    cursor = conn.cursor()

    cursor.execute("SELECT url FROM shorturls WHERE code=?", (code,))
    result = cursor.fetchone()

    cursor.close()
    conn.close()

    return generate_short_code() if result else code

def save_url(url: ShortURL):
    """Create a short URL for the given URL."""

    code: str = generate_short_code()

    conn = sqlite3.connect('shorturls.db')
    cursor = conn.cursor()

    cursor.execute("INSERT INTO shorturls (code, url) VALUES (?, ?)", (code, url.url))
    conn.commit()

    cursor.close()
    conn.close()

    return code
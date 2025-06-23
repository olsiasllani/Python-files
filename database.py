import sqlite3

def get_db():
    conn = sqlite3.connect("movies.db")
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.execute('''
    CREATE TABLE IF NOT EXISTS movies (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        director TEXT,
        year INTEGER,
        genre TEXT,
        rating INTEGER CHECK(rating BETWEEN 1 AND 5)
    )
    ''')
    conn.commit()
    conn.close()

init_db()

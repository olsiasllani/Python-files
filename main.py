from fastapi import FastAPI, HTTPException
from schemas import Movie, MovieOut
from database import get_db

app = FastAPI()

@app.post("/movies/", response_model=MovieOut)
def add_movie(movie: Movie):
    conn = get_db()
    try:
        cursor = conn.execute(
            "INSERT INTO movies (title, director, year, genre, rating) VALUES (?, ?, ?, ?, ?)",
            (movie.title, movie.director, movie.year, movie.genre, movie.rating)
        )
        conn.commit()
        movie_id = cursor.lastrowid
        return {**movie.dict(), "id": movie_id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        conn.close()

@app.get("/movies/", response_model=list[MovieOut])
def get_movies():
    conn = get_db()
    rows = conn.execute("SELECT * FROM movies").fetchall()
    conn.close()
    return [dict(row) for row in rows]

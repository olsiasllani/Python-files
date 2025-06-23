from pydantic import BaseModel

class Movie(BaseModel):
    title: str
    director: str
    year: int
    genre: str
    rating: int

class MovieOut(Movie):
    id: int

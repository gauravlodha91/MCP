import sqlite3
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

DB_NAME = "movies.db"

def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS movies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                year INTEGER,
                director TEXT,
                genre TEXT
            )
        ''')
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM movies")
        if cur.fetchone()[0] == 0:
            movies_to_add = [
                ("The Godfather", 1972, "Francis Ford Coppola", "Crime"),
                ("Pulp Fiction", 1994, "Quentin Tarantino", "Crime"),
                ("Inception", 2010, "Christopher Nolan", "Sci-Fi"),
                ("The Shawshank Redemption", 1994, "Frank Darabont", "Drama"),
                ("The Dark Knight", 2008, "Christopher Nolan", "Action"),
                ("Forrest Gump", 1994, "Robert Zemeckis", "Drama"),
                ("The Matrix", 1999, "The Wachowskis", "Sci-Fi"),
                ("Fight Club", 1999, "David Fincher", "Drama"),
                ("Interstellar", 2014, "Christopher Nolan", "Sci-Fi"),
                ("Parasite", 2019, "Bong Joon-ho", "Thriller"),
                ("Gladiator", 2000, "Ridley Scott", "Action"),
                ("Schindler's List", 1993, "Steven Spielberg", "History"),
                ("The Lion King", 1994, "Roger Allers, Rob Minkoff", "Animation"),
                ("Goodfellas", 1990, "Martin Scorsese", "Crime"),
                ("The Silence of the Lambs", 1991, "Jonathan Demme", "Thriller")
            ]
            conn.executemany(
                "INSERT INTO movies (title, year, director, genre) VALUES (?, ?, ?, ?)",
                movies_to_add
            )

class MovieIn(BaseModel):
    title: str
    year: Optional[int] = None
    director: Optional[str] = None
    genre: Optional[str] = None

class Movie(MovieIn):
    id: int

app = FastAPI(title="Movie MCP Server", description="A simple movie database API for MCP")

# Add CORS middleware for better compatibility
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup():
    init_db()
    print("Movie MCP Server started successfully!")

@app.get("/")
def root():
    return {"message": "Movie MCP server is running.", "endpoints": ["/movies", "/movies/add", "/movies/add_many", "/movies/{id}"]}

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "movie-mcp-server"}

@app.get("/movies", response_model=List[Movie])
def list_movies():
    try:
        with sqlite3.connect(DB_NAME) as conn:
            conn.row_factory = sqlite3.Row
            cur = conn.execute("SELECT * FROM movies ORDER BY id")
            movies = [Movie(**dict(row)) for row in cur.fetchall()]
            return movies
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@app.get("/movies/{movie_id}", response_model=Movie)
def get_movie(movie_id: int):
    try:
        with sqlite3.connect(DB_NAME) as conn:
            conn.row_factory = sqlite3.Row
            cur = conn.execute("SELECT * FROM movies WHERE id = ?", (movie_id,))
            row = cur.fetchone()
            if not row:
                raise HTTPException(status_code=404, detail="Movie not found")
            return Movie(**dict(row))
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@app.post("/movies/add", response_model=Movie)
def add_movie(movie: MovieIn):
    try:
        with sqlite3.connect(DB_NAME) as conn:
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO movies (title, year, director, genre) VALUES (?, ?, ?, ?)",
                (movie.title, movie.year, movie.director, movie.genre),
            )
            new_id = cur.lastrowid
            return Movie(id=new_id, **movie.dict())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@app.post("/movies/add_many", response_model=List[Movie])
def add_many_movies(movies: List[MovieIn]):
    try:
        added_movies = []
        with sqlite3.connect(DB_NAME) as conn:
            cur = conn.cursor()
            for movie in movies:
                cur.execute(
                    "INSERT INTO movies (title, year, director, genre) VALUES (?, ?, ?, ?)",
                    (movie.title, movie.year, movie.director, movie.genre),
                )
                new_id = cur.lastrowid
                added_movies.append(Movie(id=new_id, **movie.dict()))
        return added_movies
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
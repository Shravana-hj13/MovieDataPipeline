--Enable foreign key relationships
PRAGMA foreign_keys = ON;


---1. Movies Table

CREATE TABLE IF NOT EXISTS movies (

    movieId INTEGER PRIMARY KEY,

    title TEXT NOT NULL,

    release_year INTEGER,

    imdb_id TEXT,

    director TEXT,

    plot TEXT,

    imdb_rating REAL,

    runtime_minutes INTEGER,

    box_office TEXT,

    omdb_status TEXT DEFAULT 'PENDING'

);


---2. Genres Table

CREATE TABLE IF NOT EXISTS genres (

    genre_id INTEGER PRIMARY KEY AUTOINCREMENT,

    genre_name TEXT NOT NULL UNIQUE

);


---3. Movie Genres Table

CREATE TABLE IF NOT EXISTS movie_genres (

    movieId INTEGER NOT NULL,

    genre_id INTEGER NOT NULL,

    PRIMARY KEY (movieId, genre_id),

    FOREIGN KEY (movieId)
        REFERENCES movies(movieId),

    FOREIGN KEY (genre_id)
        REFERENCES genres(genre_id)

);


---4. Ratings Table

CREATE TABLE IF NOT EXISTS ratings (

    userId INTEGER NOT NULL,

    movieId INTEGER NOT NULL,

    rating REAL NOT NULL
        CHECK (rating >= 0.5 AND rating <= 5.0),

    timestamp INTEGER NOT NULL,

    PRIMARY KEY (userId, movieId),

    FOREIGN KEY (movieId)
        REFERENCES movies(movieId)

);
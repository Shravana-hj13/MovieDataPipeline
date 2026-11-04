-- 1. Highest average-rated movie

SELECT
    m.movieId,
    m.title,
    ROUND(AVG(r.rating), 2) AS average_rating,
    COUNT(r.rating) AS total_ratings
FROM movies m
JOIN ratings r
    ON m.movieId = r.movieId
GROUP BY
    m.movieId,
    m.title
ORDER BY
    average_rating DESC,
    total_ratings DESC
LIMIT 1;


-- 1.1 Highest average-rated movie
-- Considering movies with at least 50 ratings

SELECT
    m.movieId,
    m.title,
    ROUND(AVG(r.rating), 2) AS average_rating,
    COUNT(r.rating) AS total_ratings
FROM movies m
JOIN ratings r
    ON m.movieId = r.movieId
GROUP BY
    m.movieId,
    m.title
HAVING
    COUNT(r.rating) >= 50
ORDER BY
    average_rating DESC,
    total_ratings DESC
LIMIT 1;


-- 2. Top 5 Genres by Average Rating

SELECT
    g.genre_name AS genre,
    ROUND(AVG(r.rating), 2) AS average_rating,
    COUNT(r.rating) AS total_ratings
FROM genres g
JOIN movie_genres mg
    ON g.genre_id = mg.genre_id
JOIN movies m
    ON mg.movieId = m.movieId
JOIN ratings r
    ON m.movieId = r.movieId
GROUP BY
    g.genre_id,
    g.genre_name
HAVING
    COUNT(r.rating) >= 50
ORDER BY
    average_rating DESC,
    total_ratings DESC
LIMIT 5;


-- 3. Director with the Most Movies

SELECT
    director,
    COUNT(*) AS total_movies
FROM movies
WHERE director IS NOT NULL
GROUP BY director
ORDER BY total_movies DESC
LIMIT 1;


-- 4. Average Rating by Release Year

SELECT
    m.release_year,
    ROUND(AVG(r.rating), 2) AS average_rating,
    COUNT(r.rating) AS total_ratings
FROM movies m
JOIN ratings r
    ON m.movieId = r.movieId
WHERE m.release_year IS NOT NULL
GROUP BY m.release_year
ORDER BY m.release_year;
--Checking Enrichment Status

SELECT
    omdb_status,
    COUNT(*) AS total_movies
FROM movies
GROUP BY omdb_status;


--Checking available movie metadata

SELECT
    COUNT(*) AS total_movies,
    COUNT(director) AS movies_with_director,
    COUNT(imdb_rating) AS movies_with_imdb_rating,
    COUNT(release_year) AS movies_with_release_year
FROM movies;


-- PRAGMA table_info(genres);
-- PRAGMA table_info(movies);


---Movies without rating

select m.movieId, m.title, r.rating
from movies m
left join ratings r
           on m.movieId=r.movieId
where r.movieId is null
         

--Total Data Counts

SELECT
    (SELECT count(*) FROM movies) AS total_movies,
    (SELECT count(*) FROM ratings) AS total_ratings,
    (SELECT count(*) FROM genres) AS total_genres,
    (SELECT count(*) FROM movie_genres) as total_movie_genres;


import pandas as pd
from pathlib import Path
from datetime import date

#Project Directory
base_dir = Path(__file__).resolve().parent

#Dataset Paths
movies_file = base_dir / "data" / "movies.csv"
ratings_file = base_dir / "data" / "ratings.csv"

#Read CSV files
movies_df=pd.read_csv(movies_file)
ratings_df=pd.read_csv(ratings_file)

# #Display Movies Information
# print("\n========================Movies Data========================")

# print(movies_df.head())

# print("\nMovies Shape:")
# print(movies_df.shape)

# print("\nMovies Columns:")
# print(movies_df.columns)

# #Display Rating Information
# print("\n===========Ratings Data==============")

# print(ratings_df.head())

# print("\nRatings Shape:")
# print(ratings_df.shape)

# print("\nRatings Columns:");
# print(ratings_df.columns)


# #Data Quality Analysis

# print("\n================Data Quality Analysis========================")

# #1. CHecking Missing Values in Movies data
# print("\nMissing values in Movies data:")
# print(movies_df.isnull().sum())

# #2. Checking Missing Values in Ratings data
# print("\nMissing values in Ratings data:")
# print(ratings_df.isnull().sum())

# #3. Check duplicate in Movies data
# print("\nDuplicate Movies:")
# print(movies_df.duplicated().sum())

# #4. Check duplicate in Ratings data
# print("\nDuplicate Ratings:")
# print(ratings_df.duplicated().sum())

# #5. Check Movie ID Uniqueness
# print("\nUnique Movie IDs:")
# print(movies_df["movieId"].nunique())

# #6. Check Rating Distribution
# print("\nRating Distribution:")
# print(ratings_df["rating"].value_counts().sort_index())

# #7. Checking rating range
# print("\nMinimum Rating:")
# print(ratings_df["rating"].min())

# print("\nMaximum Rating:")
# print(ratings_df["rating"].max())

# #8. Check data types
# print("\n Movies data type:")
# print(movies_df.dtypes)

# print('\nRatings data type:')
# print(ratings_df.dtypes)

# print("\n================Data Quality Analysis Completed========================")

# print("\n===========Relationship Validation==============")

# #Get movieId's from Movies Dataset
# movie_ids=set(movies_df["movieId"])

# #Get movieId's from rating dataset
# rating_movie_ids=set(ratings_df["movieId"])

# #Find missing movieId's in ratings dataset but missing in Movies dataset

# missing_movie_ids=rating_movie_ids-movie_ids
# print("\nMovies referenced in ratings but missing from movies dataset:")
# print(len(missing_movie_ids))

# print("\nMissing Movie IDs:")
# print(missing_movie_ids)

# #Find movies which don't have ratings
# movies_without_ratings=movie_ids-rating_movie_ids
# print("\nMovies without ratings:")

# print(len(movies_without_ratings))
# # print(movies_without_ratings)

# print("\n========== RELATIONSHIP VALIDATION COMPLETED ==========")



#--------Creating SQLite Database---------------------
import sqlite3

#DB file path
db_file = base_dir/"movies.db"

#schema file path
schema_file = base_dir/"schema.sql"

print("\n========================Database Creation==========================")

#Connect to SQLite DB
conn=sqlite3.connect(db_file)

#Enable Foreign key relationship
conn.execute("PRAGMA foreign_keys = ON")

#Read schema.sql
with open(schema_file, "r") as file:
    schema = file.read()

#Execute SQL Schema
conn.executescript(schema)
print("Database Created Successfully!!!")

#Verify Tables
cursor = conn.cursor()

cursor.execute("""SELECT name 
               from sqlite_master 
               WHERE type='table' AND name NOT LIKE 'sqlite_%'""")

tables=cursor.fetchall()
print("\nTables Created:")

for table in tables:
    print(table[0])

#Close DB
# conn.close()


#Load Movies data

import re

print("\n========== MOVIES DATA LOADING ==========")

# Connect to database
conn = sqlite3.connect(db_file)

# Enable foreign keys
conn.execute("PRAGMA foreign_keys = ON")

cursor = conn.cursor()

# Load Movies data
movies_df = pd.read_csv(movies_file)

# Extract release year from movie title
def extract_year(title):

    match = re.search(r"\((\d{4})\)$", title)

    if match:
        return int(match.group(1))

    return None

# Extract movie title without release year

def extract_movie_title(title):

    movie_title = re.sub(
        r"\s*\(\d{4}\)$",
        "",
        title
    )

    return movie_title

# Extract release year
movies_df["release_year"] = movies_df["title"].apply(extract_year)

# Insert movies into database
movie_records = []

for _, row in movies_df.iterrows():

    movie_records.append((
        int(row["movieId"]),
        row["title"],
        row["release_year"]
    ))


cursor.executemany("""
    INSERT OR IGNORE INTO movies
    (
        movieId,
        title,
        release_year
    )
    VALUES (?, ?, ?)
""", movie_records)

conn.commit()

print("Movies inserted:", len(movie_records))


#Load Genres Data

print("\n========== GENRES DATA LOADING ==========")

genre_records = set()

movie_genre_records = []

for _, row in movies_df.iterrows():

    movie_id = int(row["movieId"])

    genres = row["genres"].split("|")

    for genre in genres:

        if genre == "(no genres listed)":
            continue

        genre_records.add(genre)

        movie_genre_records.append((
            movie_id,
            genre
        ))


# Insert unique genres
cursor.executemany("""
    INSERT OR IGNORE INTO genres
    (
        genre_name
    )
    VALUES (?)
""", [(genre,) for genre in genre_records])


conn.commit()


# Get genre IDs
cursor.execute("""
    SELECT genre_name, genre_id
    FROM genres
""")

genre_mapping = dict(cursor.fetchall())


# Insert movie-genre relationships
movie_genre_data = []

for movie_id, genre_name in movie_genre_records:

    genre_id = genre_mapping[genre_name]

    movie_genre_data.append((
        movie_id,
        genre_id
    ))


cursor.executemany("""
    INSERT OR IGNORE INTO movie_genres
    (
        movieId,
        genre_id
    )
    VALUES (?, ?)
""", movie_genre_data)


conn.commit()

print("Unique genres inserted:", len(genre_records))

print("Movie-genre relationships inserted:", len(movie_genre_data))


#Load Ratings Data

print("\n========== RATINGS DATA LOADING ==========")

# Load Ratings data
ratings_df = pd.read_csv(ratings_file)

# Prepare ratings records
rating_records = []

for _, row in ratings_df.iterrows():

    rating_records.append((
        int(row["userId"]),
        int(row["movieId"]),
        float(row["rating"]),
        int(row["timestamp"])
    ))


# Insert ratings
cursor.executemany("""
    INSERT OR IGNORE INTO ratings
    (
        userId,
        movieId,
        rating,
        timestamp
    )
    VALUES (?, ?, ?, ?)
""", rating_records)


conn.commit()

print("Ratings inserted:", len(rating_records))


#Verify DB

print("\n========== DATABASE VERIFICATION ==========")

cursor.execute("SELECT COUNT(*) FROM movies")

print("Movies in database:", cursor.fetchone()[0])


cursor.execute("SELECT COUNT(*) FROM genres")

print("Genres in database:", cursor.fetchone()[0])


cursor.execute("SELECT COUNT(*) FROM movie_genres")

print("Movie-genre relationships:", cursor.fetchone()[0])


cursor.execute("SELECT COUNT(*) FROM ratings")

print("Ratings in database:", cursor.fetchone()[0])


# Close database connection
# conn.close()

print("\n========== ETL LOADING COMPLETED ==========")


#OMDb API Test
import requests
from dotenv import load_dotenv
import os

print("\n========== OMDb API TEST ==========")

# Load environment variables
load_dotenv()

# Get API key
API_KEY = os.getenv("OMDB_API_KEY")

# Check API key
if not API_KEY:

    print("OMDb API key not found!")


# OMDb CACHE

import json

print("\n========== OMDb CACHE ==========")

# Cache file path
cache_file = base_dir / "cache" / "omdb_cache.json"


# Load existing cache
def load_cache():

    if cache_file.exists():

        with open(cache_file, "r", encoding="utf-8") as file:

            return json.load(file)

    return {}


# Save cache
def save_cache(cache):

    with open(cache_file, "w", encoding="utf-8") as file:

        json.dump(
            cache,
            file,
            indent=4
        )
        

# DAILY API REQUEST TRACKER

usage_file = base_dir / "cache" / "api_usage.json"


def load_api_usage():

    today = date.today().isoformat()

    if usage_file.exists():

        with open(usage_file, "r") as file:

            usage = json.load(file)

        if usage.get("date") == today:

            return usage.get("count", 0)

    return 0


def record_api_request():

    today = date.today().isoformat()

    current_count = load_api_usage()

    if current_count >= MAX_API_REQUESTS:

        print("Daily OMDb API request limit reached.")

        return False

    current_count += 1

    usage_file.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    usage = {
        "date": today,
        "count": current_count
    }

    with open(usage_file, "w") as file:

        json.dump(usage, file, indent=4)

    print(
        f"API requests used today: "
        f"{current_count}/{MAX_API_REQUESTS}"
    )

    return True


if usage_file.exists():

    with open(usage_file, "r") as file:

        print("Saved tracker data:", json.load(file))

print("=====================================")


# Load cache into memory
omdb_cache = load_cache()

print("Cached movies:", len(omdb_cache))

print("\n========== CACHE LOADED ==========")



# OMDb API REQUEST LIMIT

MAX_API_REQUESTS = 1000

api_requests_today = 0

print("\nDaily API limit:", MAX_API_REQUESTS)



#OMDb ENRICHMENT FUNCTION WITH CACHE

import time

print("\n========== OMDb ENRICHMENT ==========")

def get_movie_details(title, year):

    """
    Fetch movie details from OMDb.

    Uses cache to avoid repeated API requests.
    """

    # Create cache key
    cache_key = f"{title}_{year}"

    # Check cache first
    if cache_key in omdb_cache:

        print(f"Cache hit: {title}")

        return omdb_cache[cache_key]


    # Prepare API parameters

    params = {

        "t": title,

        "apikey": API_KEY

    }


    # Add year only when available

    if year is not None:

        params["y"] = int(year)


    try:
        
        # Check and record daily API usage

        if not record_api_request():

            print("Skipping API request because daily limit is reached.")

            return None


        response = requests.get(

            "https://www.omdbapi.com/",

            params=params,

            timeout=30

        )


        response.raise_for_status()


        data = response.json()


        # Movie found
        if data.get("Response") == "True":

            omdb_cache[cache_key] = data

            save_cache(omdb_cache)

            print(f"API success: {title}")

            return data


        # Movie not found
        else:

            print(f"Movie not found: {title}")

            # Save unsuccessful response in cache

            omdb_cache[cache_key] = data

            save_cache(omdb_cache)

            return data


    except requests.exceptions.RequestException as error:

        print(f"API request failed: {error}")

        return None
    

# MOVIE ENRICHMENT

print("\n========== MOVIE ENRICHMENT ==========")

MAX_REQUESTS_PER_RUN = 10

requests_before_run = load_api_usage()

print("API requests before this run:", requests_before_run)

print("Maximum new API requests this run:", MAX_REQUESTS_PER_RUN)

# Select pending movies from SQLite

cursor.execute("""

    SELECT movieId, title, release_year

    FROM movies

    WHERE omdb_status = 'PENDING'

    ORDER BY movieId

""")

movies_to_enrich = cursor.fetchall()


print("Pending movies:", len(movies_to_enrich))


# Process pending movies

for movie in movies_to_enrich:

    movie_id = movie[0]

    original_title = movie[1]

    year = movie[2]


    # Extract clean movie title

    movie_title = extract_movie_title(
        original_title
    )


    # Handle year

    if year is not None:

        year = int(year)


    print("\nProcessing:", original_title)
        
    # CHECK BATCH REQUEST LIMIT
    
    requests_used_this_run = (
        load_api_usage() - requests_before_run
    )

    if requests_used_this_run >= MAX_REQUESTS_PER_RUN:

        print("\nBatch request limit reached.")

        print("Stopping enrichment for this run.")

        break


    
    # CHECK DAILY API LIMIT
    

    if load_api_usage() >= MAX_API_REQUESTS:

        print("\nDaily API request limit reached.")

        print("Stopping movie enrichment.")

        break


    
    # FETCH OMDB DETAILS
    

    movie_data = get_movie_details(
        movie_title,
        year
    )


    # Handle unavailable movie details

    if movie_data is None:

        print("OMDb details unavailable")

        continue

    # Check whether movie was found

    if movie_data.get("Response") != "True":

        print("Movie not found in OMDb")


        cursor.execute("""

            UPDATE movies

            SET omdb_status = 'NOT_FOUND'

            WHERE movieId = ?

        """, (movie_id,))


        conn.commit()

        continue


    # Extract OMDb information

    imdb_id = movie_data.get("imdbID")

    director = movie_data.get("Director")

    plot = movie_data.get("Plot")

    imdb_rating = movie_data.get("imdbRating")

    runtime = movie_data.get("Runtime")

    box_office = movie_data.get("BoxOffice")


    # Convert IMDb rating

    if imdb_rating and imdb_rating != "N/A":

        imdb_rating = float(imdb_rating)

    else:

        imdb_rating = None


    # Convert runtime

    if runtime and runtime != "N/A":

        runtime_minutes = int(
            runtime.replace(" min", "")
        )

    else:

        runtime_minutes = None


    # Handle unavailable values

    if director == "N/A":

        director = None


    if plot == "N/A":

        plot = None


    if imdb_id == "N/A":

        imdb_id = None


    if box_office == "N/A":

        box_office = None


    # Update SQLite database

    cursor.execute("""

        UPDATE movies

        SET

            imdb_id = ?,

            director = ?,

            plot = ?,

            imdb_rating = ?,

            runtime_minutes = ?,

            box_office = ?,

            omdb_status = 'SUCCESS'

        WHERE movieId = ?

    """, (

        imdb_id,

        director,

        plot,

        imdb_rating,

        runtime_minutes,

        box_office,

        movie_id

    ))


    conn.commit()


    print("Director:", director)

    print("IMDb Rating:", imdb_rating)

    print("Runtime:", runtime_minutes)

    print("Database updated successfully")


print("\n========== ENRICHMENT COMPLETED ==========")
        

print("\n========== DATABASE VERIFICATION ==========")

cursor.execute("""

    SELECT

        movieId,

        title,

        director,

        imdb_rating,

        runtime_minutes,

        omdb_status

    FROM movies

    WHERE movieId IN (1, 2, 3, 4, 5)

""")

results = cursor.fetchall()

for row in results:

    print(row)

print("\n========== ENRICHMENT STATUS ==========")

cursor.execute("""
    SELECT
        omdb_status,
        COUNT(*)
    FROM movies
    GROUP BY omdb_status
""")

status_results = cursor.fetchall()

for row in status_results:

    print(row)
    
# Close database connection
conn.close()

print("\nDatabase connection closed.")

# Movie Data Pipeline

## Project Overview

The Movie Data Pipeline is a data engineering project that processes movie and rating data from the MovieLens dataset and enriches movie information using the OMDb API.

The project demonstrates data extraction, transformation, loading, API integration, data validation, and SQL-based analysis using Python and SQLite.

## Objectives

- Extract movie and rating data from CSV files.
- Transform and organize movie information.
- Enrich movie metadata using the OMDb API.
- Store structured data in a SQLite database.
- Track API requests to manage usage limits.
- Validate data quality and database relationships.
- Perform analytical SQL queries to identify movie and genre trends.

## Technologies Used

- Python
- SQLite
- SQL
- Pandas
- Requests
- OMDb API
- VS Code

## Dataset

The project uses the MovieLens dataset.

| Dataset Component         | Records |
| ------------------------- | ------: |
| Movies                    |   9,742 |
| Ratings                   | 100,836 |
| Genres                    |      19 |
| Movie-Genre Relationships |  22,050 |

The movie dataset contains movie titles and genre information. The ratings dataset contains user ratings associated with movies.

## Project Structure

```text
MovieDataPipeline/
│
├── data/
│   ├── movies.csv
│   └── ratings.csv
│
├── cache/
│   ├── omdb_cache.json
│   └── api_usage.json
│
├── venv/
│
├── etl.py
├── schema.sql
├── queries.sql
├── validation.sql
├── requirements.txt
├── README.md
└── .env
```

## ETL Workflow

### 1. Extract

Movie and rating data are extracted from the MovieLens CSV files.

### 2. Transform

The extracted data is processed and organized into structured database tables.

Movie metadata is enriched using the OMDb API, including available information such as director, plot, IMDb rating, runtime, and box office.

### 3. Load

The processed data is loaded into a SQLite database.

The database contains separate tables for movies, ratings, genres, and movie-genre relationships.

## Database Schema

The project uses the following tables:

### Movies

Stores movie information, including:

- Movie ID
- Title
- Release year
- IMDb ID
- Director
- Plot
- IMDb rating
- Runtime
- Box office
- OMDb enrichment status

### Ratings

Stores user ratings associated with movies.

### Genres

Stores available movie genres.

### Movie Genres

Connects movies with their corresponding genres.

## API Integration

The project uses the OMDb API to enrich movie metadata.

API request tracking and caching are implemented to reduce repeated requests and manage API usage.

The enrichment process maintains three statuses:

- `SUCCESS`: Movie metadata was successfully retrieved.
- `NOT_FOUND`: Movie information was not found through the API.
- `PENDING`: Movie metadata has not yet been processed.

### Enrichment Status

Based on the latest enrichment run:

| Status    | Movies |
| --------- | -----: |
| SUCCESS   |    613 |
| NOT_FOUND |    351 |
| PENDING   |  8,778 |
| Total     |  9,742 |

The enrichment process is partially completed. Movies marked as pending have not yet been processed.

## Data Validation

SQL queries are used to validate the database and check data quality.

Validation includes:

- Checking enrichment status.
- Checking available movie metadata.
- Identifying movies without ratings.
- Verifying database record counts.

The database contains 18 movies without associated ratings.

These records are retained because they are valid movie records in the original dataset.

## Analytical SQL Queries

The project includes the following analytical queries:

### 1. Highest-Rated Movie

Identifies the highest-rated movie among movies with at least 50 ratings.

### 2. Top 5 Genres by Average Rating

Calculates genre-wise average ratings and identifies the top five genres.

### 3. Director with the Most Movies

Identifies the director with the highest number of movies among records with available director information.

### 4. Average Rating by Release Year

Calculates average movie ratings grouped by release year.

## Database Validation Results

| Table        | Records |
| ------------ | ------: |
| Movies       |   9,742 |
| Ratings      | 100,836 |
| Genres       |      19 |
| Movie Genres |  22,050 |

The final database record counts match the expected counts from the original dataset.

## Analytical Findings

### Highest-Rated Movie

The Shawshank Redemption (1994)

- Average rating: 4.43
- Total ratings: 317

### Top-Rated Genre

Film-Noir

- Average rating: 3.92
- Total ratings: 870

### Director with the Most Movies

Alfred Hitchcock

- Movies: 10

## How to Run the Project

### 1. Clone the Repository

```bash
git clone <your-github-repository-url>
```

### 2. Navigate to the Project

```bash
cd MovieDataPipeline
```

### 3. Create a Virtual Environment

```bash
python -m venv venv
```

### 4. Activate the Virtual Environment

Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### 5. Install Dependencies

```bash
pip install -r requirements.txt
```

### 6. Configure Environment Variables

Create a `.env` file and configure your OMDb API key.

Do not publish your API key in the repository.

### 7. Run the ETL Pipeline

```bash
python etl.py
```

The pipeline processes the data and stores it in the SQLite database.

## SQL Files

- `schema.sql`: Database table definitions.
- `queries.sql`: Analytical SQL queries.
- `validation.sql`: Data validation queries.

## Future Improvements

- Complete the remaining movie metadata enrichment.
- Improve data quality checks.
- Add more analytical SQL queries.
- Build a dashboard to visualize movie ratings and genre trends.
- Automate pipeline execution.

## Author

Movie Data Pipeline Project

## License

This project is intended for educational and portfolio purposes.

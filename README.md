# Spotify Listening History Analyzer

A personal project that loads my full Spotify streaming history into a PostgreSQL database and analyzes my listening habits.

## What it does

- Loads my full Spotify streaming history (multiple years, multiple JSON files) into a PostgreSQL database
- Structures the data into artists, tracks and play history — including timestamps, play duration, skips and shuffle state
- Analyzes and visualizes the data with Python and matplotlib

## Analysis

So far:
- Top 10 most played artists (bar chart)

Things I want to add:
- Favorite songs by play count
- Listening time per artist
- Time of day listening patterns
- Genre breakdown via Spotify API

## Tech stack

- **Python** — data loading and analysis
- **PostgreSQL** — data storage
- **psycopg2** — Python/PostgreSQL connection
- **matplotlib** — data visualization
- **Spotify GDPR export** — data source

## How to run it yourself

### 1. Get your Spotify data
You can request your extended streaming history at [spotify.com/account/privacy](https://www.spotify.com/account/privacy/). 
It takes up to 30 days (for me it took much shorter tho). You'll get a few of JSON files named like `Streaming_History_Audio_2023_0.json`.

### 2. Set up PostgreSQL
You'll need PostgreSQL running locally with a database called `music_habits`. 
Update the connection details in the scripts to match your setup.

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Load the data
Drop your Spotify JSON files in the project folder and run:
```bash
python3 load_spotify.py
```

### 5. Run the analysis
```bash
python3 analyse_spotify.py
```

## Note on data privacy
My Spotify JSON files are gitignored so no personal data is uploaded here, just the code.
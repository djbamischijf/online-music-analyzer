## TODO
- [ ] Favorite songs by minutes listened
- [ ] Determine genre of songs via Spotify API. Then determine favorite genre per time of the day to do different music recommendations depending on the time of day.
- [ ] Filter out plays under 30 seconds

## Dashboard

[View the interactive dashboard on Tableau Public](https://public.tableau.com/views/SpotifyLuistergedrag/Spotifyluistergedrag2011-2026)

## Data pipeline

1. **Spotify export** — JSON files with full streaming history
2. **Python (`load_spotify.py`)** — loads and structures the data into PostgreSQL
3. **PostgreSQL** — stores the data in different tables (artists, tracks, listening_history)
4. **SQL (`export_for_dashboard.sql`)** — joins the tables and exports a single table as CSV
5. **Tableau** — dashboard with visualizations

## Tech stack

- **Python** — data loading (psycopg2)
- **PostgreSQL** — data storage
- **SQL** — data transformation and analysis
- **Tableau** — dashboarding and visualization
- **matplotlib** — additional analysis

## How to run it yourself

### 1. Get your Spotify data
You can request your extended streaming history at [spotify.com/account/privacy](https://www.spotify.com/account/privacy/).
It takes up to 30 days (for me it took much shorter tho). You'll get a few JSON files named like `Streaming_History_Audio_2023_0.json`.

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

### 5. Export for dashboard
Run the query in `export_for_dashboard.sql` in DBeaver and export the result as CSV.

### 6. Run the analysis
```bash
python3 analyse_history.py
```

## Note on personal data
My Spotify JSON files are not included in this repository.
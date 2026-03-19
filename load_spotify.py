import json
import psycopg2
import glob

# --- Load JSON files ---
spotify_data = []
for filepath in glob.glob('Streaming_History_Audio_*.json'):
    with open(filepath, 'r') as f:
        data = json.load(f)
        spotify_data.extend(data)
        print(f"Loaded {len(data)} plays from {filepath}")

print(f"Total plays loaded: {len(spotify_data)}")

# --- Connect to database ---
conn = psycopg2.connect(
    dbname='music_habits',
    user='timofranssen',
    host='localhost',
    port=5432
)

cursor = conn.cursor()
print('Connected!')

# --- Create tables ---
cursor.execute("""
    CREATE TABLE IF NOT EXISTS artists (
        artist_id SERIAL PRIMARY KEY,
        name TEXT NOT NULL,
        platform TEXT,
        spotify_id TEXT,
        genres TEXT[]
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS tracks (
        track_id SERIAL PRIMARY KEY,
        artist_id INTEGER REFERENCES artists(artist_id),
        title TEXT NOT NULL,
        platform TEXT,
        spotify_uri TEXT
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS listening_history (
        history_id SERIAL PRIMARY KEY,
        track_id INTEGER REFERENCES tracks(track_id),
        played_at TIMESTAMP,
        ms_played INTEGER,
        platform TEXT,
        skipped BOOLEAN,
        shuffle BOOLEAN,
        reason_end TEXT
    )
""")

conn.commit()
print("Tables ready!")

# --- Empty tables in case they already exist ---
cursor.execute("TRUNCATE TABLE listening_history RESTART IDENTITY CASCADE")
cursor.execute("TRUNCATE TABLE tracks RESTART IDENTITY CASCADE")
cursor.execute("TRUNCATE TABLE artists RESTART IDENTITY CASCADE")
conn.commit()
print("Tables emptied!")

# --- Insert artists ---
artist_names = set()
for song in spotify_data:
    if song['master_metadata_album_artist_name']:  # can be null for podcasts
        artist_names.add(song['master_metadata_album_artist_name'])

for artist_name in artist_names:
    cursor.execute(
        "INSERT INTO artists (name, platform) VALUES (%s, %s) ON CONFLICT DO NOTHING",
        (artist_name, 'Spotify')
    )
conn.commit()
print(f"Artists inserted: {len(artist_names)}")

# --- Insert tracks ---
tracks = set()
for song in spotify_data:
    if song['master_metadata_track_name'] and song['master_metadata_album_artist_name']:
        tracks.add((
            song['master_metadata_album_artist_name'],
            song['master_metadata_track_name'],
            song['spotify_track_uri']
        ))

for artist_name, track_title, spotify_uri in tracks:
    cursor.execute("SELECT artist_id FROM artists WHERE name = %s", (artist_name,))
    artist_id = cursor.fetchone()[0]
    cursor.execute(
        "INSERT INTO tracks (artist_id, title, spotify_uri, platform) VALUES (%s, %s, %s, %s)",
        (artist_id, track_title, spotify_uri, 'Spotify')
    )
conn.commit()
print(f"Tracks inserted: {len(tracks)}")

# --- Insert listening history ---
for play in spotify_data:
    if not play['master_metadata_track_name'] or not play['master_metadata_album_artist_name']:
        continue  # skip podcasts/audiobooks

    cursor.execute("SELECT artist_id FROM artists WHERE name = %s",
        (play['master_metadata_album_artist_name'],))
    artist_id = cursor.fetchone()[0]

    cursor.execute("SELECT track_id FROM tracks WHERE title = %s AND artist_id = %s",
        (play['master_metadata_track_name'], artist_id))
    track_id = cursor.fetchone()[0]

    cursor.execute("""
        INSERT INTO listening_history
            (track_id, played_at, ms_played, platform, skipped, shuffle, reason_end)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (
        track_id,
        play['ts'],
        play['ms_played'],
        play['platform'],
        play['skipped'],
        play['shuffle'],
        play['reason_end']
    ))

conn.commit()
print("Listening history inserted!")

cursor.close()
conn.close()

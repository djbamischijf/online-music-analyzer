import json
with open('sample_spotify_data.json', 'r') as f:
    spotify_data = json.load(f)

import psycopg2

conn = psycopg2.connect(
    dbname='music_habits',
    user='timofranssen',
    host='localhost',
    port=5432
)

cursor = conn.cursor()
print('Connected!')

artist_names = set()
for song in spotify_data:
     artist_names.add(song['master_metadata_album_artist_name'])
print("Set with artists created!")

for artist_name in artist_names:
    cursor.execute("INSERT INTO artists (name, platform) VALUES (%s, %s)", (artist_name, 'Spotify'))
    conn.commit()
print('Artists inserted!')

tracks = set()
for song in spotify_data:
    artist_name = song['master_metadata_album_artist_name']
    track_title = song['master_metadata_track_name']
    tracks.add((artist_name, track_title))
print("Set with tracks created!")

for artist_name, track_title in tracks:
    cursor.execute("SELECT artist_id FROM artists WHERE name = %s", (artist_name,))
    artist_id = cursor.fetchone()[0]
    cursor.execute("INSERT INTO tracks (artist_id, title, platform) VALUES (%s, %s, %s)", (artist_id, track_title, 'Spotify'))
    conn.commit()
print('Songs inserted!')

for play in spotify_data:
    track_title = play['master_metadata_track_name']
    artist_name = play['master_metadata_album_artist_name']
    cursor.execute("SELECT artist_id FROM artists WHERE name = %s", (artist_name,))
    artist_id = cursor.fetchone()[0]
    cursor.execute("SELECT track_id FROM tracks WHERE title = %s AND artist_id = %s", (track_title, artist_id))
    track_id = cursor.fetchone()[0]
    cursor.execute("INSERT INTO listening_history (track_id, played_at, platform) VALUES (%s, %s, %s)", (track_id, play['ts'], 'Spotify'))
    conn.commit()
print('Play inserted!')
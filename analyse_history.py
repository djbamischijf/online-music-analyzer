import psycopg2
import matplotlib.pyplot as plt

conn = psycopg2.connect(
    dbname='music_habits',
    user='timofranssen',
    host='localhost',
    port=5432
)
cursor = conn.cursor()

cursor.execute("""
    SELECT a.name, COUNT(*) AS play_count
    FROM listening_history lh
    JOIN tracks t ON lh.track_id = t.track_id
    JOIN artists a ON t.artist_id = a.artist_id
    GROUP BY a.name
    ORDER BY play_count DESC
    LIMIT 10
""")
rows = cursor.fetchall()

artists = [row[0] for row in rows]
play_counts = [row[1] for row in rows]

plt.figure(figsize=(12, 6))
plt.barh(artists[::-1], play_counts[::-1])
plt.xlabel('Number of plays')
plt.title('My top 10 most played artists')
plt.tight_layout()
plt.show()

cursor.close()
conn.close()
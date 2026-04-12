-- Combine the three tables (listening_history, tracks, artists) into a single table for visualization in Tableau. Export the result as CSV via DBeaver.
SELECT lh.played_at,
       EXTRACT(YEAR FROM lh.played_at) AS year,
       EXTRACT(HOUR FROM lh.played_at) AS hour,
       TO_CHAR(lh.played_at, 'Day') AS day_of_week,
       a.name AS artist, 
       t.title AS track, 
       lh.ms_played,
       ROUND(lh.ms_played / 60000.0, 2) AS minutes_played,
       lh.skipped,
       lh.shuffle
FROM listening_history lh
JOIN tracks t ON lh.track_id = t.track_id
JOIN artists a ON t.artist_id = a.artist_id;
-- Q6: Calculate the average danceability of tracks in each album
SELECT album, AVG(danceability) as avg_danceability
FROM spotify
GROUP BY album
ORDER BY avg_danceability DESC;

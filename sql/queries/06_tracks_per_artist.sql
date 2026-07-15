-- Q5: Count the total number of tracks by each artist
SELECT artist, COUNT(*) as track_count
FROM spotify
GROUP BY artist
ORDER BY track_count DESC;

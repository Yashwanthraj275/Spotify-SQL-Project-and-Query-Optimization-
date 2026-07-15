-- Q9: For each album, calculate the total views of all associated tracks
SELECT track, SUM(views) as total_views
FROM spotify
GROUP BY track
ORDER BY total_views DESC;

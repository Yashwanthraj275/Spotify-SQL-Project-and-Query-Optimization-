-- Q11: Find the top 3 most-viewed tracks for each artist using window functions
WITH ranking_artist AS (
    SELECT 
        artist,
        track,
        SUM(views) as total_view,
        DENSE_RANK() OVER (PARTITION BY artist ORDER BY SUM(views) DESC) as rank
    FROM spotify
    GROUP BY artist, track
)
SELECT * FROM ranking_artist
WHERE rank <= 3
ORDER BY artist, rank;

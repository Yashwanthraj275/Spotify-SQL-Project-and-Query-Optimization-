-- Q15: Calculate the cumulative sum of likes for tracks ordered by the number of views, using window functions
SELECT
    track,
    artist,
    views,
    likes,
    SUM(likes) OVER (
        ORDER BY views DESC
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) AS cumulative_likes
FROM spotify
ORDER BY views DESC;

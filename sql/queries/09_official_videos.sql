-- Q8: List all tracks along with their views and likes where official_video = TRUE
SELECT track, SUM(views) as sum_views, SUM(likes) as sum_likes
FROM spotify
WHERE official_video = true
GROUP BY track
ORDER BY sum_views DESC;

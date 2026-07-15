-- Q3: Get the total number of comments for tracks where licensed = TRUE
SELECT SUM(comments) as total_comments
FROM spotify
WHERE licensed = true;

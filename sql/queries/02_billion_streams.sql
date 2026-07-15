-- Q1: Retrieve the names of all tracks that have more than 1 billion streams
SELECT track, stream
FROM spotify
WHERE stream > 1000000000
ORDER BY stream DESC;

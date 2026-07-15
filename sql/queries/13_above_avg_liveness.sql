-- Q12: Write a query to find tracks where the liveness score is above the average
SELECT track, artist, liveness
FROM spotify
WHERE liveness > (SELECT AVG(liveness) FROM spotify)
ORDER BY liveness DESC;

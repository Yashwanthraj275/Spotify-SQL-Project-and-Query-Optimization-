-- Q7: Find the top 5 tracks with the highest energy values
SELECT track, artist, MAX(energy) as max_energy
FROM spotify
GROUP BY track, artist
ORDER BY max_energy DESC
LIMIT 5;

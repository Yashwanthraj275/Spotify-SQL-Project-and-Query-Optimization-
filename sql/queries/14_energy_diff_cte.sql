-- Q13: Use a WITH clause to calculate the difference between the highest and lowest energy values for tracks in each album
WITH energy_stats AS (
    SELECT 
        album,
        MAX(energy) as highest_energy,
        MIN(energy) as lowest_energy
    FROM spotify
    GROUP BY album
)
SELECT 
    album,
    highest_energy - lowest_energy as energy_diff
FROM energy_stats
ORDER BY energy_diff DESC;

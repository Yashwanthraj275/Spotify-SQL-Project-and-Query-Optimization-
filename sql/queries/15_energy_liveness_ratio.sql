-- Q14: Find tracks where the energy-to-liveness ratio is greater than 1.2
SELECT track, artist, energy, liveness, (energy / NULLIF(liveness, 0)) as ene_liv_ratio
FROM spotify
WHERE (energy / NULLIF(liveness, 0)) > 1.2
ORDER BY ene_liv_ratio DESC;

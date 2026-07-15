-- Q4: Find all tracks that belong to the album type single
SELECT track, artist, album
FROM spotify
WHERE album_type = 'single'
ORDER BY artist, track;

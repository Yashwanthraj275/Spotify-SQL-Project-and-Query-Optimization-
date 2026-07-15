-- Q10: Retrieve the track names that have been streamed on Spotify more than YouTube
SELECT track, spotify_streams, youtube_streams
FROM (
    SELECT track,
           COALESCE(SUM(CASE WHEN most_played_on = 'Spotify' THEN stream END), 0) as spotify_streams,
           COALESCE(SUM(CASE WHEN most_played_on = 'Youtube' THEN stream END), 0) as youtube_streams
    FROM spotify
    GROUP BY track
) subquery
WHERE spotify_streams > youtube_streams AND youtube_streams > 0
ORDER BY spotify_streams DESC;

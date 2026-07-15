-- Optimization: Create indexes on frequently queried columns
-- These indexes dramatically improve query performance for equality and range searches

CREATE INDEX IF NOT EXISTS idx_artist ON spotify(artist);
-- Improves: Q2, Q5, Q11 (artist lookups)

CREATE INDEX IF NOT EXISTS idx_stream ON spotify(stream DESC);
-- Improves: Q1 (billion-stream filter)

CREATE INDEX IF NOT EXISTS idx_album ON spotify(album);
-- Improves: Q6, Q13 (album aggregations)

CREATE INDEX IF NOT EXISTS idx_album_type ON spotify(album_type);
-- Improves: Q4 (single/album filtering)

CREATE INDEX IF NOT EXISTS idx_most_played_on ON spotify(most_played_on);
-- Improves: Q10 (platform comparison)

CREATE INDEX IF NOT EXISTS idx_licensed ON spotify(licensed);
-- Improves: Q3 (licensed track filtering)

CREATE INDEX IF NOT EXISTS idx_official_video ON spotify(official_video);
-- Improves: Q8 (official video filtering)

-- Composite indexes for common filter combinations
CREATE INDEX IF NOT EXISTS idx_artist_stream ON spotify(artist, stream DESC);
-- Improves: Q1 + artist filtering

CREATE INDEX IF NOT EXISTS idx_album_danceability ON spotify(album, danceability);
-- Improves: Q6 (album + danceability queries)

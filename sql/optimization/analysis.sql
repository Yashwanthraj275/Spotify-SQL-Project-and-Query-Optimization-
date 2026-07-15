-- Performance Analysis: EXPLAIN ANALYZE for key queries
-- Run these to see execution plans and understand optimization opportunities

-- IMPORTANT: Create indexes first!
-- psql -U postgres -d spotify -f sql/optimization/indexes.sql

-- Query 1: Artist lookup (PRIMARY OPTIMIZATION CASE STUDY)
-- Before index: 7 ms, Planning: 0.17 ms (Sequential Scan)
-- After index: 0.153 ms, Planning: 0.152 ms (Index Scan)
EXPLAIN ANALYZE SELECT * FROM spotify WHERE artist = 'Taylor Swift';

-- Query 2: Billion-stream tracks
EXPLAIN ANALYZE SELECT * FROM spotify WHERE stream > 1000000000;

-- Query 3: Album aggregation
EXPLAIN ANALYZE SELECT album, AVG(danceability) as avg_danceability FROM spotify GROUP BY album;

-- Query 4: Top artist by views (window function)
EXPLAIN ANALYZE 
WITH ranking_artist AS (
    SELECT 
        artist,
        track,
        SUM(views) as total_view,
        DENSE_RANK() OVER (PARTITION BY artist ORDER BY SUM(views) DESC) as rank
    FROM spotify
    GROUP BY artist, track
)
SELECT * FROM ranking_artist WHERE rank <= 3 LIMIT 10;

-- Check all indexes
\di

-- Check table statistics
SELECT schemaname, tablename, indexname, idx_scan, idx_tup_read, idx_tup_fetch 
FROM pg_stat_user_indexes;

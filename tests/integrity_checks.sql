-- 1. Check for tracks with 0 or negative duration (Data anomaly check)
SELECT CASE 
    WHEN COUNT(*) > 0 THEN 'FAIL: Table contains invalid track durations'
    ELSE 'PASS: All track durations are valid'
END AS test_duration
FROM spotify 
WHERE duration_min <= 0;

-- 2. Verify dataset loading (Basic row count check)
SELECT CASE 
    WHEN COUNT(*) = 0 THEN 'FAIL: No records found. Data loading failed!'
    ELSE 'PASS: Data loaded successfully'
END AS test_data_load
FROM spotify;

-- 3. Check for duplicates in critical identifier groupings
SELECT artist, track, COUNT(*) 
FROM spotify 
GROUP BY artist, track 
HAVING COUNT(*) > 1;

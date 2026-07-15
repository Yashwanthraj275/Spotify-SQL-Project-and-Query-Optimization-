-- Exploratory Data Analysis (EDA)
-- Get overview of the dataset

SELECT COUNT(*) as total_tracks FROM spotify;

SELECT COUNT(DISTINCT artist) as unique_artists FROM spotify;

SELECT COUNT(DISTINCT album) as unique_albums FROM spotify;

SELECT DISTINCT album_type FROM spotify;

SELECT MAX(duration_min) as max_duration, MIN(duration_min) as min_duration FROM spotify;

SELECT DISTINCT channel FROM spotify;

SELECT DISTINCT most_played_on FROM spotify;

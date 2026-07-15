import pytest
import psycopg2
from psycopg2.extras import RealDictCursor
import os

@pytest.fixture
def db_conn():
    """Connect to PostgreSQL database"""
    conn = psycopg2.connect(
        host=os.getenv('PGHOST', 'localhost'),
        port=os.getenv('PGPORT', '5432'),
        database=os.getenv('POSTGRES_DB', 'spotify'),
        user=os.getenv('POSTGRES_USER', 'postgres'),
        password=os.getenv('POSTGRES_PASSWORD', 'postgres')
    )
    yield conn
    conn.close()

@pytest.fixture
def cursor(db_conn):
    """Create database cursor"""
    cur = db_conn.cursor(cursor_factory=RealDictCursor)
    yield cur
    cur.close()


# ============================================================================
# QUERY VALIDATION TESTS
# ============================================================================

class TestQueryExecution:
    """Tests to ensure all queries execute without errors"""
    
    def test_01_eda_query_executes(self, cursor):
        """Q1: EDA query should return results"""
        cursor.execute("SELECT COUNT(*) as total_tracks FROM spotify;")
        result = cursor.fetchone()
        assert result['total_tracks'] > 0, "EDA query should return track count"
    
    def test_02_billion_streams_query(self, cursor):
        """Q2: Should find tracks with >1 billion streams"""
        cursor.execute("SELECT track, stream FROM spotify WHERE stream > 1000000000 ORDER BY stream DESC;")
        results = cursor.fetchall()
        # At least some tracks should have >1B streams
        assert len(results) > 0, "Should find tracks with >1B streams"
        assert all(r['stream'] > 1000000000 for r in results), "All results should have >1B streams"
    
    def test_03_albums_artists_query(self, cursor):
        """Q3: Should return album-artist pairs"""
        cursor.execute("SELECT DISTINCT album, artist FROM spotify ORDER BY album;")
        results = cursor.fetchall()
        assert len(results) > 0, "Should return album-artist pairs"
        assert all('album' in r and 'artist' in r for r in results), "Should have album and artist columns"
    
    def test_04_licensed_comments_query(self, cursor):
        """Q4: Should calculate total comments for licensed tracks"""
        cursor.execute("SELECT SUM(comments) as total_comments FROM spotify WHERE licensed = true;")
        result = cursor.fetchone()
        assert result is not None, "Licensed comments query should return result"
    
    def test_05_single_albums_query(self, cursor):
        """Q5: Should find single album type tracks"""
        cursor.execute("SELECT track, artist, album FROM spotify WHERE album_type = 'single' ORDER BY artist, track;")
        results = cursor.fetchall()
        assert len(results) > 0, "Should find single type albums"
        assert all(r for r in results), "All results should be valid"
    
    def test_06_tracks_per_artist_query(self, cursor):
        """Q6: Should count tracks by artist"""
        cursor.execute("SELECT artist, COUNT(*) as track_count FROM spotify GROUP BY artist ORDER BY track_count DESC;")
        results = cursor.fetchall()
        assert len(results) > 0, "Should have artist track counts"
        assert all(r['track_count'] > 0 for r in results), "All counts should be positive"
    
    def test_07_avg_danceability_query(self, cursor):
        """Q7: Should calculate average danceability per album"""
        cursor.execute("SELECT album, AVG(danceability) as avg_danceability FROM spotify GROUP BY album ORDER BY avg_danceability DESC;")
        results = cursor.fetchall()
        assert len(results) > 0, "Should have album danceability data"
    
    def test_08_top_energy_query(self, cursor):
        """Q8: Should find top 5 high-energy tracks"""
        cursor.execute("SELECT track, artist, MAX(energy) as max_energy FROM spotify GROUP BY track, artist ORDER BY max_energy DESC LIMIT 5;")
        results = cursor.fetchall()
        assert len(results) == 5, "Should return exactly 5 top energy tracks"
        assert all(r['max_energy'] > 0 for r in results), "Energy should be positive"
    
    def test_09_official_videos_query(self, cursor):
        """Q9: Should find official video stats"""
        cursor.execute("SELECT track, SUM(views) as sum_views, SUM(likes) as sum_likes FROM spotify WHERE official_video = true GROUP BY track ORDER BY sum_views DESC;")
        results = cursor.fetchall()
        assert len(results) >= 0, "Official videos query should execute"
    
    def test_10_spotify_vs_youtube_query(self, cursor):
        """Q10: Should compare Spotify vs YouTube streams"""
        cursor.execute("""
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
        """)
        results = cursor.fetchall()
        assert len(results) >= 0, "Should compare platforms"
        if len(results) > 0:
            assert all(r['spotify_streams'] > r['youtube_streams'] for r in results), "Spotify should be > YouTube"
    
    def test_11_top_tracks_window_function(self, cursor):
        """Q11: Should use window functions to find top 3 tracks per artist"""
        cursor.execute("""
            WITH ranking_artist AS (
                SELECT 
                    artist,
                    track,
                    SUM(views) as total_view,
                    DENSE_RANK() OVER (PARTITION BY artist ORDER BY SUM(views) DESC) as rank
                FROM spotify
                GROUP BY artist, track
            )
            SELECT * FROM ranking_artist
            WHERE rank <= 3
            ORDER BY artist, rank
            LIMIT 10;
        """)
        results = cursor.fetchall()
        assert len(results) > 0, "Window function should return results"
        assert all(r['rank'] <= 3 for r in results), "All ranks should be <= 3"
    
    def test_12_above_avg_liveness_query(self, cursor):
        """Q12: Should find tracks above average liveness"""
        cursor.execute("""
            SELECT track, artist, liveness
            FROM spotify
            WHERE liveness > (SELECT AVG(liveness) FROM spotify)
            ORDER BY liveness DESC;
        """)
        results = cursor.fetchall()
        assert len(results) > 0, "Should find tracks above average liveness"
    
    def test_13_energy_diff_cte(self, cursor):
        """Q13: CTE should calculate energy difference per album"""
        cursor.execute("""
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
        """)
        results = cursor.fetchall()
        assert len(results) > 0, "CTE should return energy statistics"
    
    def test_14_energy_liveness_ratio(self, cursor):
        """Q14: Should find tracks with energy/liveness ratio > 1.2"""
        cursor.execute("""
            SELECT track, artist, energy, liveness, (energy / NULLIF(liveness, 0)) as ene_liv_ratio
            FROM spotify
            WHERE (energy / NULLIF(liveness, 0)) > 1.2
            ORDER BY ene_liv_ratio DESC;
        """)
        results = cursor.fetchall()
        assert len(results) >= 0, "Query should execute"
        if len(results) > 0:
            assert all(r['ene_liv_ratio'] > 1.2 for r in results), "All ratios should be > 1.2"
    
    def test_15_cumulative_likes_window(self, cursor):
        """Q15: Window function for cumulative sum of likes"""
        cursor.execute("""
            SELECT
                track,
                artist,
                views,
                likes,
                SUM(likes) OVER (
                    ORDER BY views DESC
                    ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
                ) AS cumulative_likes
            FROM spotify
            ORDER BY views DESC
            LIMIT 10;
        """)
        results = cursor.fetchall()
        assert len(results) > 0, "Window function should calculate cumulative sum"
        assert all('cumulative_likes' in r for r in results), "Should have cumulative_likes column"


# ============================================================================
# INDEX PERFORMANCE TESTS
# ============================================================================

class TestIndexing:
    """Tests to verify indexes exist and improve performance"""
    
    def test_artist_index_exists(self, cursor):
        """Artist index should exist"""
        cursor.execute("""
            SELECT COUNT(*) as count 
            FROM pg_indexes 
            WHERE schemaname = 'public' 
            AND tablename = 'spotify' 
            AND indexname = 'idx_artist';
        """)
        result = cursor.fetchone()
        assert result['count'] == 1, "idx_artist index must exist"
    
    def test_stream_index_exists(self, cursor):
        """Stream index should exist for billion-stream queries"""
        cursor.execute("""
            SELECT COUNT(*) as count 
            FROM pg_indexes 
            WHERE schemaname = 'public' 
            AND tablename = 'spotify' 
            AND indexname = 'idx_stream';
        """)
        result = cursor.fetchone()
        assert result['count'] == 1, "idx_stream index must exist"
    
    def test_album_index_exists(self, cursor):
        """Album index should exist"""
        cursor.execute("""
            SELECT COUNT(*) as count 
            FROM pg_indexes 
            WHERE schemaname = 'public' 
            AND tablename = 'spotify' 
            AND indexname = 'idx_album';
        """)
        result = cursor.fetchone()
        assert result['count'] == 1, "idx_album index must exist"
    
    def test_all_optimization_indexes_exist(self, cursor):
        """All optimization indexes should be created"""
        expected_indexes = [
            'idx_artist',
            'idx_stream',
            'idx_album',
            'idx_album_type',
            'idx_most_played_on',
            'idx_licensed',
            'idx_official_video',
            'idx_artist_stream',
            'idx_album_danceability'
        ]
        
        for idx_name in expected_indexes:
            cursor.execute(f"""
                SELECT COUNT(*) as count 
                FROM pg_indexes 
                WHERE schemaname = 'public' 
                AND tablename = 'spotify' 
                AND indexname = '{idx_name}';
            """)
            result = cursor.fetchone()
            assert result['count'] == 1, f"Index {idx_name} must exist"
    
    def test_artist_lookup_uses_index(self, cursor):
        """Artist lookup should use index efficiently"""
        cursor.execute("""
            EXPLAIN (ANALYZE, FORMAT JSON) 
            SELECT * FROM spotify WHERE artist = 'The Weeknd' LIMIT 1;
        """)
        plan = cursor.fetchone()
        # Should use index scan, not sequential scan
        plan_text = str(plan)
        assert 'Index Scan' in plan_text or 'index' in plan_text.lower(), "Should use index for artist lookup"


# ============================================================================
# DATA INTEGRITY TESTS
# ============================================================================

class TestDataIntegrity:
    """Tests to verify data quality"""
    
    def test_no_zero_duration_tracks(self, cursor):
        """No tracks should have 0 duration"""
        cursor.execute("SELECT COUNT(*) as count FROM spotify WHERE duration_min = 0;")
        result = cursor.fetchone()
        assert result['count'] == 0, "No tracks should have 0 duration"
    
    def test_stream_values_positive(self, cursor):
        """Stream counts should be non-negative"""
        cursor.execute("SELECT COUNT(*) as count FROM spotify WHERE stream < 0;")
        result = cursor.fetchone()
        assert result['count'] == 0, "No tracks should have negative streams"
    
    def test_no_null_artist_names(self, cursor):
        """Artist names should not be null"""
        cursor.execute("SELECT COUNT(*) as count FROM spotify WHERE artist IS NULL;")
        result = cursor.fetchone()
        assert result['count'] == 0, "No null artist names"
    
    def test_danceability_in_valid_range(self, cursor):
        """Danceability should be between 0 and 1"""
        cursor.execute("SELECT COUNT(*) as count FROM spotify WHERE danceability < 0 OR danceability > 1;")
        result = cursor.fetchone()
        assert result['count'] == 0, "Danceability should be 0-1"
    
    def test_energy_in_valid_range(self, cursor):
        """Energy should be between 0 and 1"""
        cursor.execute("SELECT COUNT(*) as count FROM spotify WHERE energy < 0 OR energy > 1;")
        result = cursor.fetchone()
        assert result['count'] == 0, "Energy should be 0-1"


# ============================================================================
# AGGREGATION CORRECTNESS TESTS
# ============================================================================

class TestAggregations:
    """Tests to verify aggregation queries are correct"""
    
    def test_artist_track_count_accuracy(self, cursor):
        """Track count per artist should match total"""
        cursor.execute("""
            SELECT SUM(track_count) as total_from_agg FROM (
                SELECT COUNT(*) as track_count FROM spotify GROUP BY artist
            ) t;
        """)
        agg_total = cursor.fetchone()['total_from_agg']
        
        cursor.execute("SELECT COUNT(*) as total FROM spotify;")
        actual_total = cursor.fetchone()['total']
        
        assert agg_total == actual_total, "Artist aggregation should match total track count"
    
    def test_group_by_album_type_valid(self, cursor):
        """Album types should be valid categories"""
        cursor.execute("SELECT DISTINCT album_type FROM spotify WHERE album_type NOT IN ('single', 'album');")
        invalid = cursor.fetchall()
        assert len(invalid) == 0, "Album types should only be 'single' or 'album'"

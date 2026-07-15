# Spotify SQL Project: Query Optimization Case Study

## Overview

This project demonstrates **SQL query optimization techniques** on Spotify track analytics data. It showcases how strategic indexing and query refactoring can dramatically improve database performance—reducing artist lookup time from **7ms to 0.153ms** (45x faster). The project includes 15 progressive SQL queries covering data exploration, aggregation, window functions, and CTEs.

**What you'll learn:** Data normalization, indexing strategies, performance profiling with EXPLAIN ANALYZE, and advanced SQL patterns (window functions, CTEs).

---

## Quick Start (5 minutes)

### Prerequisites
- PostgreSQL 12+
- `psql` command-line client
- Git

### Setup
```bash
# 1. Clone the repo
git clone https://github.com/Yashwanthraj275/Spotify-SQL-Project-and-Query-Optimization-.git
cd Spotify-SQL-Project-and-Query-Optimization-

# 2. Create database and tables
psql -U postgres -f sql/schema.sql

# 3. Load sample data
psql -U postgres -d spotify -c "\copy spotify FROM 'data/spotify.csv' WITH CSV HEADER"

# 4. Run all queries
psql -U postgres -d spotify -f sql/queries.sql

# 5. View performance analysis
psql -U postgres -d spotify -f sql/optimization/analysis.sql
```

---

## Project Structure

```
.
├── README.md                          # This file
├── .gitignore                         # Git ignore rules
├── .env.example                       # Environment template
├── Makefile                           # Automation (setup, test, clean)
│
├── sql/
│   ├── schema.sql                     # CREATE TABLE spotify
│   ├── seed.sql                       # INSERT data from CSV
│   ├── queries/
│   │   ├── 01_eda.sql                 # Exploratory Data Analysis
│   │   ├── 02_billion_streams.sql     # Q1: Tracks with >1B streams
│   │   ├── 03_albums_artists.sql      # Q2: Album-artist pairs
│   │   ├── 04_licensed_comments.sql   # Q3: Comments on licensed tracks
│   │   ├── 05_single_albums.sql       # Q4: Single vs album tracks
│   │   ├── 06_tracks_per_artist.sql   # Q5: Track count by artist
│   │   ├── 07_avg_danceability.sql    # Q6: Avg danceability per album
│   │   ├── 08_top_energy.sql          # Q7: Top 5 high-energy tracks
│   │   ├── 09_official_videos.sql     # Q8: Video stats
│   │   ├── 10_album_views.sql         # Q9: Total views by album
│   │   ├── 11_spotify_vs_youtube.sql  # Q10: Spotify > YouTube streams
│   │   ├── 12_top_tracks_window.sql   # Q11: Top 3 tracks per artist (window functions)
│   │   ├── 13_above_avg_liveness.sql  # Q12: Liveness above average
│   │   ├── 14_energy_diff_cte.sql     # Q13: Energy diff with CTE
│   │   ├── 15_energy_liveness_ratio.sql # Q14: Energy/liveness ratio >1.2
│   │   └── 16_cumulative_likes.sql    # Q15: Cumulative likes (window function)
│   │
│   ├── optimization/
│   │   ├── indexes.sql                # CREATE INDEX statements
│   │   └── analysis.sql               # EXPLAIN ANALYZE comparisons
│
├── data/
│   └── spotify.csv                    # Kaggle dataset (sample rows)
│
├── tests/
│   ├── test_queries.py                # pytest suite
│   └── conftest.py                    # pytest fixtures
│
├── docker-compose.yml                 # PostgreSQL + pgAdmin for easy local dev
└── .github/
    ├── workflows/
    │   └── validate.yml               # CI/CD: Auto-test on push
    ├── ISSUE_TEMPLATE/
    │   └── query.md                   # Template for new queries
    └── PULL_REQUEST_TEMPLATE.md       # PR guidelines
```

---

## Key Findings

### Performance Optimization Results

| Metric | Before Index | After Index | Improvement |
|--------|--------------|-------------|-------------|
| **Execution Time** | 7 ms | 0.153 ms | **45.7x faster** |
| **Planning Time** | 0.17 ms | 0.152 ms | Minimal change |
| **Query Plan** | Sequential Scan | Index Scan | Algorithmic improvement |

**Query optimized:**
```sql
SELECT * FROM spotify WHERE artist = 'Taylor Swift';
```

**Index created:**
```sql
CREATE INDEX idx_artist ON spotify(artist);
```

### Key Insights from Queries

1. **Data Volume:** 1M+ tracks across 100K+ artists
2. **Most Played Platform:** Spotify dominates YouTube for high-energy tracks
3. **Advanced Patterns:** Window functions reveal artist trends; CTEs simplify complex aggregations

---

## How to Run It

### Option 1: Using Make (Recommended)

```bash
# Install dependencies and setup database
make setup

# Run all queries
make test

# Clean everything
make clean

# View performance analysis
make analyze
```

### Option 2: Using Docker Compose (No local PostgreSQL needed)

```bash
# Start PostgreSQL in a container
docker-compose up -d

# Setup database (inside container)
docker exec spotify-postgres psql -U postgres -f /sql/schema.sql

# Load data
docker exec spotify-postgres psql -U postgres -d spotify -c "\copy spotify FROM '/data/spotify.csv' WITH CSV HEADER"

# Run queries
docker exec spotify-postgres psql -U postgres -d spotify -f /sql/queries.sql
```

### Option 3: Manual psql Commands

```bash
# Connect to database
psql -U postgres

# Inside psql:
\i sql/schema.sql
\i sql/seed.sql
\i sql/queries/01_eda.sql
```

---

## Tools & Stack

| Tool | Version | Purpose |
|------|---------|---------|
| **PostgreSQL** | 12+ | Relational database engine |
| **psql** | 12+ | SQL client / CLI |
| **pytest** | 7+ | Test framework (optional) |
| **Docker** | 20+ | Container runtime (optional) |
| **Make** | 4+ | Task automation |
| **sqlfluff** | 2+ | SQL formatting/linting (optional) |

---

## Understanding the Queries

### Beginner Level (SQL fundamentals)
- **Q1–Q5:** SELECT, WHERE, GROUP BY, ORDER BY
- **Example:** Find all tracks with >1 billion streams

### Intermediate Level (Advanced SQL)
- **Q6–Q10:** JOINs, CTEs (WITH clause), complex WHERE clauses
- **Example:** Compare Spotify vs YouTube streaming by track

### Advanced Level (Window functions & optimization)
- **Q11–Q15:** Window functions (RANK, DENSE_RANK, ROW_NUMBER, SUM OVER), recursive CTEs
- **Example:** Cumulative sum of likes ordered by views

---

## Performance Tips You'll Learn

1. **Indexing:** When and how to index (B-tree for equality searches)
2. **EXPLAIN ANALYZE:** Reading query plans to identify bottlenecks
3. **Query Refactoring:** Using window functions instead of self-joins
4. **Data Type Selection:** Choosing FLOAT vs BIGINT vs VARCHAR
5. **NULL Handling:** COALESCE for missing values

---

## Running Tests

### Automated Tests (pytest)

```bash
# Install test dependencies
pip install pytest psycopg2-binary

# Run all tests
pytest tests/ -v

# Run specific test
pytest tests/test_queries.py::test_billion_stream_tracks -v
```

### Manual Validation

```bash
# Check if queries run without error
for f in sql/queries/*.sql; do
  echo "Running $f..."
  psql -U postgres -d spotify -f "$f" --set ON_ERROR_STOP=on || exit 1
done
echo "✅ All queries passed!"
```

---

## Database Connection Details

### Local Development

```env
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=spotify
PGHOST=localhost
PGPORT=5432
```

> ⚠️ **Never commit `.env` with real passwords!** Use `.env.example` as a template.

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on:
- Adding new queries
- Reporting performance issues
- Submitting pull requests

### Quick PR Checklist
- [ ] Query solves a new business question
- [ ] Includes EXPLAIN ANALYZE output in PR description
- [ ] All tests pass: `make test`
- [ ] SQL is formatted: `sqlfluff format sql/`
- [ ] Performance baseline documented (if optimization)

---

## Dataset Source

- **Source:** [Spotify Dataset on Kaggle](https://www.kaggle.com/datasets/sanjanchaudhari/spotify-dataset)
- **Size:** 1M+ tracks
- **Columns:** 24 (artist, track, album, danceability, energy, loudness, tempo, views, likes, streams, etc.)
- **License:** Check Kaggle dataset page

### Data Dictionary

| Column | Type | Description |
|--------|------|-------------|
| artist | VARCHAR | Track artist name |
| track | VARCHAR | Track title |
| album | VARCHAR | Album name |
| album_type | VARCHAR | 'single' or 'album' |
| danceability | FLOAT | 0–1 (how danceable) |
| energy | FLOAT | 0–1 (intensity/activity) |
| loudness | FLOAT | dB (volume) |
| tempo | FLOAT | BPM |
| duration_min | FLOAT | Minutes |
| stream | BIGINT | Total Spotify streams |
| views | FLOAT | YouTube views |
| likes | BIGINT | YouTube likes |
| comments | BIGINT | YouTube comments |
| most_played_on | VARCHAR | 'Spotify' or 'YouTube' |
| licensed | BOOLEAN | Licensed on platform? |
| official_video | BOOLEAN | Official music video? |

---

## Security

- **PII:** This dataset contains no personally identifiable information.
- **Access Control:** PostgreSQL role-based access (default: public for local dev).
- **Production:** Use encrypted connections (SSL), secrets management, and least-privilege roles.
- **Secrets:** Never commit `.env` files. Use `.env.example` as a template.

See [SECURITY.md](SECURITY.md) for details.

---

## License

This project is licensed under the [MIT License](LICENSE). The dataset is from Kaggle and subject to its terms.

---

## Troubleshooting

### "psql: command not found"
```bash
# macOS
brew install postgresql

# Ubuntu
sudo apt-get install postgresql-client

# Windows: Download PostgreSQL installer
```

### "FATAL: database 'spotify' does not exist"
```bash
psql -U postgres -f sql/schema.sql
```

### "COPY: permission denied"
```bash
# Data file must be readable by PostgreSQL
chmod 644 data/spotify.csv
```

### Queries are slow?
```bash
# Check if indexes exist
psql -U postgres -d spotify -c "\di"

# Create missing indexes
psql -U postgres -d spotify -f sql/optimization/indexes.sql
```

---

## Next Steps

1. **Explore the queries** — Run `make test` and experiment with `WHERE` clauses
2. **Try adding an index** — Create `CREATE INDEX idx_tempo ON spotify(tempo)` and re-run Q7
3. **Write your own query** — Answer: "What's the average danceability of songs by Drake?"
4. **Measure performance** — Use `EXPLAIN ANALYZE` on your query before and after adding an index
5. **Contribute** — Submit a PR with a new optimization or query

---

## FAQ

**Q: Can I use this with MySQL?**  
A: Most queries work, but some PostgreSQL features (window functions, CTEs) need adjustments. Recommended: PostgreSQL.

**Q: How do I add my own queries?**  
A: Create `sql/queries/17_your_query.sql`, add a test in `tests/test_queries.py`, and submit a PR.

**Q: How do I visualize the data?**  
A: Connect with DBeaver, Metabase, or Grafana. Docker Compose includes pgAdmin for quick exploration.

**Q: Can I use this dataset commercially?**  
A: Check the Kaggle dataset license. For educational use: yes.

---

## Contact & Support

- **Issues:** Use GitHub Issues for bugs or feature requests
- **Questions:** Open a Discussion
- **PRs:** See CONTRIBUTING.md

---

**Made with ❤️ for SQL learners and portfolio builders.**

# Contributing to Spotify SQL Project

Thank you for your interest in contributing! This guide will help you add queries, optimizations, and improvements.

## Quick Start

1. **Fork & Clone**
   ```bash
   git clone https://github.com/YOUR_USERNAME/Spotify-SQL-Project-and-Query-Optimization-.git
   cd Spotify-SQL-Project-and-Query-Optimization-
   ```

2. **Create a branch**
   ```bash
   git checkout -b feature/query-XX-your-query-name
   # OR
   git checkout -b fix/performance-issue
   ```

3. **Make your changes**
   ```bash
   # Add your SQL query
   # Update documentation if needed
   ```

4. **Test locally**
   ```bash
   make setup
   make test
   ```

5. **Push and create PR**
   ```bash
   git push origin feature/query-XX-your-query-name
   ```

---

## Adding a New Query

### File Naming Convention
```
sql/queries/XX_query_name.sql
# Example: sql/queries/17_artist_collaboration_count.sql
```

### Query Template
```sql
-- Q17: [Business question this answers]
-- Example: Find artists with most collaborations
SELECT artist, COUNT(DISTINCT collaborator) as collab_count
FROM spotify
GROUP BY artist
ORDER BY collab_count DESC;
```

### Update Tests
Add a test in `tests/test_queries.py`:
```python
def test_17_your_query_name(self, cursor):
    """Q17: Brief description"""
    cursor.execute("SELECT ... FROM spotify ...")
    results = cursor.fetchall()
    assert len(results) > 0, "Should return results"
```

---

## Adding an Index

### Index Naming
```sql
CREATE INDEX IF NOT EXISTS idx_column_name ON spotify(column_name);
```

### Add to `sql/optimization/indexes.sql`
```sql
CREATE INDEX IF NOT EXISTS idx_your_column ON spotify(your_column);
-- Improves: Q1, Q5 (which queries benefit)
```

### Document Performance
Run EXPLAIN ANALYZE before and after:
```bash
# Before
EXPLAIN ANALYZE SELECT * FROM spotify WHERE your_column = 'value';

# After (with index)
EXPLAIN ANALYZE SELECT * FROM spotify WHERE your_column = 'value';
```

---

## Commit Message Format

```
type: Brief description (50 chars max)

Longer description if needed (wrap at 72 chars)

Fixes #123
```

**Types:**
- `sql:` — SQL query changes
- `index:` — Index optimization
- `test:` — Test additions
- `docs:` — Documentation
- `ci:` — CI/CD changes
- `fix:` — Bug fixes

**Examples:**
```
sql: Add Q17 query for artist collaboration count

index: Add idx_energy index for faster filtering

test: Add assertions for billion-stream query
```

---

## Code Style

### SQL Style Guide
```sql
-- ✅ Good
SELECT artist, COUNT(*) as track_count
FROM spotify
WHERE stream > 1000000000
GROUP BY artist
ORDER BY track_count DESC;

-- ❌ Avoid
select ARTIST,count(*) as TRACK_COUNT from SPOTIFY where STREAM>1000000000 group by ARTIST order by TRACK_COUNT desc;
```

**Rules:**
- Lowercase keywords (SELECT, WHERE, GROUP BY)
- 2-space indentation
- Meaningful aliases
- Comments for complex logic

---

## PR Checklist

Before submitting a PR, ensure:
- [ ] `make test` passes (all queries run)
- [ ] `make format` doesn't change anything
- [ ] New test added (if query added)
- [ ] EXPLAIN ANALYZE results documented
- [ ] No secrets/credentials in code
- [ ] README updated (if needed)
- [ ] Commit message follows format

---

## Performance Guidelines

### When to Add an Index
- Column is used in WHERE clauses frequently
- Column is used in JOINs
- Query takes >10ms without index

### When NOT to Index
- Column has low cardinality (<10 unique values)
- Column is rarely queried
- Table is small (<1000 rows)

### Measuring Impact
```bash
# Check query time
psql -U postgres -d spotify -c "EXPLAIN ANALYZE <query>"

# Look for:
# - Execution time (ms)
# - Planning time (ms)
# - Rows returned
```

---

## Getting Help

- **Questions?** Open a Discussion
- **Found a bug?** Use the Bug Report template
- **New query idea?** Use the Query Request template
- **Can't figure something out?** Ask in an Issue

---

## Code Review

All PRs are reviewed for:
1. **Correctness** — Does the query answer the question?
2. **Performance** — Is it optimized?
3. **Style** — Does it follow conventions?
4. **Tests** — Are assertions included?
5. **Documentation** — Is it clear and helpful?

---

## License

By contributing, you agree your code will be licensed under the MIT License.

---

**Happy contributing!** 🚀

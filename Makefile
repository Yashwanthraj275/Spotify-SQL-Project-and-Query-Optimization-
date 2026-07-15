.PHONY: help setup seed test analyze clean format lint

help:
	@echo "📚 Spotify SQL Project - Available Commands"
	@echo ""
	@echo "  make setup      - Initialize PostgreSQL & create schema"
	@echo "  make seed       - Load CSV data into database"
	@echo "  make test       - Run all SQL queries (validation)"
	@echo "  make analyze    - Show EXPLAIN ANALYZE for key queries"
	@echo "  make format     - Format SQL files with sqlfluff"
	@echo "  make lint       - Lint SQL files"
	@echo "  make clean      - Drop database & cleanup"
	@echo "  make help       - Show this help message"
	@echo ""

setup:
	@echo "🚀 Setting up PostgreSQL database..."
	@psql -U $(POSTGRES_USER) -h $(PGHOST) -p $(PGPORT) -f sql/schema.sql
	@echo "✅ Schema created successfully!"

seed:
	@echo "📥 Loading Spotify data..."
	@psql -U $(POSTGRES_USER) -d $(POSTGRES_DB) -h $(PGHOST) -p $(PGPORT) -c "\copy spotify FROM 'data/spotify.csv' WITH CSV HEADER"
	@echo "✅ Data loaded successfully!"

test:
	@echo "🧪 Running all SQL queries..."
	@for f in sql/queries/*.sql; do \
		echo "  Running $$f..."; \
		psql -U $(POSTGRES_USER) -d $(POSTGRES_DB) -h $(PGHOST) -p $(PGPORT) -f $$f --set ON_ERROR_STOP=on || exit 1; \
	done
	@echo "✅ All queries passed!"

analyze:
	@echo "📊 Running EXPLAIN ANALYZE..."
	@psql -U $(POSTGRES_USER) -d $(POSTGRES_DB) -h $(PGHOST) -p $(PGPORT) -f sql/optimization/analysis.sql

format:
	@echo "🎨 Formatting SQL files..."
	@command -v sqlfluff >/dev/null 2>&1 || { echo "❌ sqlfluff not installed. Run: pip install sqlfluff"; exit 1; }
	@sqlfluff format sql/ --dialect postgres
	@echo "✅ SQL formatted!"

lint:
	@echo "🔍 Linting SQL files..."
	@command -v sqlfluff >/dev/null 2>&1 || { echo "❌ sqlfluff not installed. Run: pip install sqlfluff"; exit 1; }
	@sqlfluff lint sql/ --dialect postgres

clean:
	@echo "🧹 Cleaning up..."
	@psql -U $(POSTGRES_USER) -h $(PGHOST) -p $(PGPORT) -c "DROP DATABASE IF EXISTS $(POSTGRES_DB);"
	@echo "✅ Database dropped!"

.DEFAULT_GOAL := help

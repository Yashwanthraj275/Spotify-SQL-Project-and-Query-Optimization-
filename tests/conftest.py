"""
Pytest configuration and fixtures for Spotify SQL project tests.
Run tests with: pytest tests/ -v
"""

import pytest
import psycopg2
import os
import sys

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


def pytest_configure(config):
    """Configure pytest markers"""
    config.addinivalue_line(
        "markers", "query: mark test as a query validation test"
    )
    config.addinivalue_line(
        "markers", "index: mark test as an index performance test"
    )
    config.addinivalue_line(
        "markers", "integrity: mark test as a data integrity test"
    )
    config.addinivalue_line(
        "markers", "aggregation: mark test as an aggregation correctness test"
    )


@pytest.fixture(scope="session")
def db_config():
    """Get database configuration from environment or defaults"""
    return {
        'host': os.getenv('PGHOST', 'localhost'),
        'port': int(os.getenv('PGPORT', '5432')),
        'database': os.getenv('POSTGRES_DB', 'spotify'),
        'user': os.getenv('POSTGRES_USER', 'postgres'),
        'password': os.getenv('POSTGRES_PASSWORD', 'postgres'),
    }


@pytest.fixture(scope="session")
def db_connection_session(db_config):
    """Session-scoped database connection"""
    try:
        conn = psycopg2.connect(**db_config)
        print(f"\n✅ Connected to PostgreSQL at {db_config['host']}:{db_config['port']}/{db_config['database']}")
        yield conn
        conn.close()
    except psycopg2.Error as e:
        print(f"\n❌ Failed to connect to database: {e}")
        pytest.skip(f"Database connection failed: {e}")


@pytest.fixture
def db_conn(db_connection_session):
    """Function-scoped database connection using session connection"""
    return db_connection_session


@pytest.fixture
def cursor(db_conn):
    """Get a database cursor"""
    cur = db_conn.cursor()
    yield cur
    cur.close()


@pytest.fixture(autouse=True)
def reset_after_test(db_conn):
    """Commit any pending transactions after each test"""
    yield
    db_conn.commit()


def pytest_collection_modifyitems(config, items):
    """Add markers to tests based on their names"""
    for item in items:
        if "query" in item.nodeid:
            item.add_marker(pytest.mark.query)
        if "index" in item.nodeid:
            item.add_marker(pytest.mark.index)
        if "integrity" in item.nodeid:
            item.add_marker(pytest.mark.integrity)
        if "aggregation" in item.nodeid:
            item.add_marker(pytest.mark.aggregation)

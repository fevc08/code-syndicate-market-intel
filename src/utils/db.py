# src/utils/db.py
"""
Database connection module for Code Syndicate Market Intelligence.
Provides SQLAlchemy engine and connection utilities.
"""

from sqlalchemy import create_engine, text
from src.utils.config import config

_engine = None


def get_engine():
    """
    Returns the SQLAlchemy engine.
    Creates it on first call (lazy initialization).
    Subsequent calls return the same engine instance.
    """
    global _engine
    if _engine is None:
        _engine = create_engine(config.db_url)
    return _engine


def test_connection() -> bool:
    """
    Tests that the database connection works.
    Returns True if successful, False otherwise.
    """
    try:
        engine = get_engine()
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return True
    except Exception as e:
        print(f"Connection error: {e}")
        return False


if __name__ == "__main__":
    if test_connection():
        print("✅ Database connection successful")
    else:
        print("❌ Database connection failed")
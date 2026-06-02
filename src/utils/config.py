# src/utils/config.py
"""
Configuration module for Code Syndicate Market Intelligence.
Reads environment variables from .env file and exposes them
as a typed configuration object.
"""

import os
from dotenv import load_dotenv

load_dotenv(override=True)


class Config:
    """
    Central configuration object.
    Reads from environment variables on instantiation.
    Raises ValueError if required variables are missing.
    """
    def __init__(self):
        self.db_host = self._require("DB_HOST")
        self.db_port = os.getenv("DB_PORT", "5432")
        self.db_name = self._require("DB_NAME")
        self.db_user = self._require("DB_USER")
        self.db_password = self._require("DB_PASSWORD")
        self.user_agent = (
            "code-syndicate-market-intel/0.1 "
            "(fevera@codesyndicatelatam.com)"
        )
        self.rate_limit_seconds = 1.0

    def _require(self, key: str) -> str:
        """
        Helper method: reads an env variable and raises
        ValueError if it's missing or empty.
        """
        value = os.getenv(key)
        if not value:
            raise ValueError(
                f"Required environment variable '{key}' is missing. "
                f"Check your .env file."
            )
        return value

    @property
    def db_url(self) -> str:
        """
        Returns the SQLAlchemy database URL.
        Format: postgresql://user:password@host:port/dbname
        """
        return f"postgresql://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"


config = Config()
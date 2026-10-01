import sqlite3
from datetime import datetime

from models.weather_cache_entry import WeatherCacheEntry


DEFAULT_DB_PATH = "/srv/meshdata/databases/hawaiimeshnode.db"


class WeatherCacheRepository:
    def __init__(self, db_path=DEFAULT_DB_PATH):
        self.db_path = db_path

    def initialize(self):
        with sqlite3.connect(self.db_path) as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS weather_cache (
                    cache_key TEXT PRIMARY KEY,
                    data_type TEXT NOT NULL,
                    payload TEXT NOT NULL,
                    source_time TEXT NOT NULL,
                    retrieved_at TEXT NOT NULL,
                    expires_at TEXT NOT NULL
                )
                """
            )

    def save(self, entry):
        with sqlite3.connect(self.db_path) as connection:
            connection.execute(
                """
                INSERT INTO weather_cache (
                    cache_key,
                    data_type,
                    payload,
                    source_time,
                    retrieved_at,
                    expires_at
                )
                VALUES (?, ?, ?, ?, ?, ?)
                ON CONFLICT(cache_key) DO UPDATE SET
                    data_type = excluded.data_type,
                    payload = excluded.payload,
                    source_time = excluded.source_time,
                    retrieved_at = excluded.retrieved_at,
                    expires_at = excluded.expires_at
                """,
                (
                    entry.cache_key,
                    entry.data_type,
                    entry.payload,
                    entry.source_time.isoformat(),
                    entry.retrieved_at.isoformat(),
                    entry.expires_at.isoformat(),
                ),
            )

    def get(self, cache_key):
        with sqlite3.connect(self.db_path) as connection:
            row = connection.execute(
                """
                SELECT
                    cache_key,
                    data_type,
                    payload,
                    source_time,
                    retrieved_at,
                    expires_at
                FROM weather_cache
                WHERE cache_key = ?
                """,
                (cache_key,),
            ).fetchone()

        if row is None:
            return None

        return WeatherCacheEntry(
            cache_key=row[0],
            data_type=row[1],
            payload=row[2],
            source_time=datetime.fromisoformat(row[3]),
            retrieved_at=datetime.fromisoformat(row[4]),
            expires_at=datetime.fromisoformat(row[5]),
        )
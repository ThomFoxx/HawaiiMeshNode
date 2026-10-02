import sqlite3
from datetime import datetime, timezone
from pathlib import Path


DEFAULT_DB_PATH = Path("/srv/meshdata/databases/hawaiimeshnode.db")


class ZipRequestRepository:
    def __init__(self, db_path=DEFAULT_DB_PATH):
        self.db_path = Path(db_path)

    def initialize(self):
        self.db_path.parent.mkdir(parents=True, exist_ok=True)

        with sqlite3.connect(self.db_path) as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS zip_requests (
                    zip_code TEXT PRIMARY KEY,
                    request_count INTEGER NOT NULL DEFAULT 0,
                    last_requested TEXT NOT NULL
                )
                """
            )

    def record_request(self, zip_code):
        requested_at = datetime.now(timezone.utc).isoformat()

        with sqlite3.connect(self.db_path) as connection:
            connection.execute(
                """
                INSERT INTO zip_requests (
                    zip_code,
                    request_count,
                    last_requested
                )
                VALUES (?, 1, ?)
                ON CONFLICT(zip_code)
                DO UPDATE SET
                    request_count = request_count + 1,
                    last_requested = excluded.last_requested
                """,
                (zip_code, requested_at),
            )

    def get_request_count(self, zip_code):
        with sqlite3.connect(self.db_path) as connection:
            row = connection.execute(
                """
                SELECT request_count
                FROM zip_requests
                WHERE zip_code = ?
                """,
                (zip_code,),
            ).fetchone()

        if row is None:
            return 0

        return row[0]

    def get_most_requested(self, limit=10):
        with sqlite3.connect(self.db_path) as connection:
            rows = connection.execute(
                """
                SELECT zip_code, request_count, last_requested
                FROM zip_requests
                ORDER BY request_count DESC, last_requested DESC
                LIMIT ?
                """,
                (limit,),
            ).fetchall()

        return rows

    def get_recently_requested(self, cutoff, limit=5):
        with sqlite3.connect(self.db_path) as connection:
            rows = connection.execute(
                """
                SELECT zip_code
                FROM zip_requests
                WHERE last_requested >= ?
                ORDER BY
                    request_count DESC,
                    last_requested DESC
                LIMIT ?
                """,
                (
                    cutoff.isoformat(),
                    limit,
                ),
            ).fetchall()

        return [row[0] for row in rows]
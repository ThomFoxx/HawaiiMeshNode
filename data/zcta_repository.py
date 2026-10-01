import sqlite3
from pathlib import Path
from models.zip_location import ZipLocation


DEFAULT_DB_PATH = Path("/srv/meshdata/databases/hawaiimeshnode.db")


class ZctaRepository:
    def __init__(self, db_path=DEFAULT_DB_PATH):
        self.db_path = Path(db_path)

    def initialize(self):
        self.db_path.parent.mkdir(parents=True, exist_ok=True)

        with sqlite3.connect(self.db_path) as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS zcta_locations (
                    zip_code TEXT PRIMARY KEY,
                    latitude REAL NOT NULL,
                    longitude REAL NOT NULL,
                    land_area INTEGER NOT NULL,
                    water_area INTEGER NOT NULL
                )
                """
            )

    def save(
        self,
        zip_code,
        latitude,
        longitude,
        land_area,
        water_area,
    ):
        with sqlite3.connect(self.db_path) as connection:
            connection.execute(
                """
                INSERT INTO zcta_locations (
                    zip_code,
                    latitude,
                    longitude,
                    land_area,
                    water_area
                )
                VALUES (?, ?, ?, ?, ?)
                ON CONFLICT(zip_code)
                DO UPDATE SET
                    latitude = excluded.latitude,
                    longitude = excluded.longitude,
                    land_area = excluded.land_area,
                    water_area = excluded.water_area
                """,
                (
                    zip_code,
                    latitude,
                    longitude,
                    land_area,
                    water_area,
                ),
            )

    def get(self, zip_code):
        with sqlite3.connect(self.db_path) as connection:
            row = connection.execute(
                """
                SELECT
                    zip_code,
                    latitude,
                    longitude,
                    land_area,
                    water_area
                FROM zcta_locations
                WHERE zip_code = ?
                """,
                (zip_code,),
            ).fetchone()

        if row is None:
            return None

        return ZipLocation(
            zip_code=row[0],
            latitude=row[1],
            longitude=row[2],
            land_area=row[3],
            water_area=row[4],
        )

    def save_many(self, rows):
        with sqlite3.connect(self.db_path) as connection:
            connection.executemany(
                """
                INSERT INTO zcta_locations (
                    zip_code,
                    latitude,
                    longitude,
                    land_area,
                    water_area
                )
                VALUES (?, ?, ?, ?, ?)
                ON CONFLICT(zip_code)
                DO UPDATE SET
                    latitude = excluded.latitude,
                    longitude = excluded.longitude,
                    land_area = excluded.land_area,
                    water_area = excluded.water_area
                """,
                rows,
            )
import csv
from pathlib import Path

from data.zcta_repository import ZctaRepository


SOURCE_DIR = Path("/srv/meshdata/reference/zcta/2026")


def find_source_file():
    files = list(SOURCE_DIR.glob("*.txt"))

    if len(files) == 0:
        raise FileNotFoundError("No ZCTA Gazetteer text file found.")

    if len(files) > 1:
        raise RuntimeError("More than one ZCTA Gazetteer text file found.")

    return files[0]


def import_zcta():
    source_file = find_source_file()

    repository = ZctaRepository()
    repository.initialize()

    rows = []

    with source_file.open(
        "r",
        encoding="utf-8-sig",
        newline="",
    ) as file:
        reader = csv.DictReader(file, delimiter="|")

        for raw_row in reader:
            row = {
                key.strip(): value.strip()
                for key, value in raw_row.items()
            }

            rows.append(
                (
                    row["GEOID"],
                    float(row["INTPTLAT"]),
                    float(row["INTPTLONG"]),
                    int(row["ALAND"]),
                    int(row["AWATER"]),
                )
            )

    repository.save_many(rows)

    print(f"Imported {len(rows)} ZCTA locations.")


if __name__ == "__main__":
    import_zcta()
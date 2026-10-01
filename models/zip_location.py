from dataclasses import dataclass


@dataclass(frozen=True)
class ZipLocation:
    zip_code: str
    latitude: float
    longitude: float
    land_area: int
    water_area: int
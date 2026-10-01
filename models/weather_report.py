from dataclasses import dataclass


@dataclass(frozen=True)
class WeatherReport:
    region_code: str
    region_name: str
    summary: str
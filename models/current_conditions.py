from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class CurrentConditions:
    station_id: str
    station_name: str
    time_zone: str
    observed_at: datetime
    description: str | None

    temperature_f: float | None
    dewpoint_f: float | None
    humidity_percent: float | None

    wind_direction_degrees: float | None
    wind_direction_compass: str | None
    wind_speed_mph: float | None
    wind_gust_mph: float | None

    visibility_miles: float | None
    pressure_inhg: float | None
    precipitation_last_hour_in: float | None

    source: str
    raw_message: str | None
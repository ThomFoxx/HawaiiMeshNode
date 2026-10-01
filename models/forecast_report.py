from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class ForecastReport:
    region_code: str
    time_zone: str
    generated_at: datetime
    period_name: str
    start_time: datetime
    end_time: datetime
    temperature: int | None
    temperature_unit: str | None
    wind_direction: str | None
    wind_speed: str | None
    precipitation_chance: int | None
    short_forecast: str | None
    detailed_forecast: str | None
    source: str
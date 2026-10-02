from dataclasses import dataclass

from models.current_conditions import CurrentConditions
from models.forecast_report import ForecastReport


@dataclass(frozen=True)
class WeatherResult:
    data: CurrentConditions | ForecastReport
    is_stale: bool
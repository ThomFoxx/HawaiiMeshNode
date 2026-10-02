import json
from dataclasses import asdict
from datetime import datetime, timedelta, timezone

from data.weather_cache_repository import WeatherCacheRepository
from models.current_conditions import CurrentConditions
from models.forecast_report import ForecastReport
from models.weather_cache_entry import WeatherCacheEntry


CURRENT_TTL = timedelta(minutes=10)
FORECAST_TTL = timedelta(minutes=30)

CURRENT_STALE_MAX = timedelta(hours=6)
FORECAST_STALE_MAX = timedelta(hours=24)

CACHE_RETENTION = timedelta(days=7)


class WeatherCacheService:
    def __init__(self, repository=None):
        self.repository = (
            repository
            if repository is not None
            else WeatherCacheRepository()
        )

        self.repository.initialize()

    def get_current(self, cache_key):
        entry = self.repository.get(cache_key)

        if entry is None:
            return None

        now = datetime.now(timezone.utc)

        if entry.is_expired(now):
            return None

        return self._deserialize_current(
            entry.payload
        )

    def get_current_stale(self, cache_key):
        entry = self.repository.get(cache_key)

        if entry is None:
            return None

        now = datetime.now(timezone.utc)

        if now - entry.source_time > CURRENT_STALE_MAX:
            return None

        return self._deserialize_current(
            entry.payload
        )

    def save_current(self, cache_key, conditions):
        now = datetime.now(timezone.utc)

        payload = asdict(conditions)

        payload["observed_at"] = (
            conditions.observed_at.isoformat()
        )

        entry = WeatherCacheEntry(
            cache_key=cache_key,
            data_type="CURRENT",
            payload=json.dumps(payload),
            source_time=conditions.observed_at,
            retrieved_at=now,
            expires_at=now + CURRENT_TTL,
        )

        self.repository.save(entry)

    def get_forecast(self, cache_key):
        entry = self.repository.get(cache_key)

        if entry is None:
            return None

        now = datetime.now(timezone.utc)

        if entry.is_expired(now):
            return None

        return self._deserialize_forecast(
            entry.payload
        )

    def get_forecast_stale(self, cache_key):
        entry = self.repository.get(cache_key)

        if entry is None:
            return None

        now = datetime.now(timezone.utc)

        if (
            now - entry.retrieved_at
            > FORECAST_STALE_MAX
        ):
            return None

        return self._deserialize_forecast(
            entry.payload
        )

    def save_forecast(self, cache_key, forecast):
        now = datetime.now(timezone.utc)

        payload = asdict(forecast)

        payload["generated_at"] = (
            forecast.generated_at.isoformat()
        )

        payload["start_time"] = (
            forecast.start_time.isoformat()
        )

        payload["end_time"] = (
            forecast.end_time.isoformat()
        )

        entry = WeatherCacheEntry(
            cache_key=cache_key,
            data_type="FORECAST",
            payload=json.dumps(payload),
            source_time=forecast.generated_at,
            retrieved_at=now,
            expires_at=now + FORECAST_TTL,
        )

        self.repository.save(entry)

    def cleanup(self):
        cutoff = (
            datetime.now(timezone.utc)
            - CACHE_RETENTION
        )

        return self.repository.delete_older_than(
            cutoff
        )

    def _deserialize_current(self, payload):
        data = json.loads(payload)

        return CurrentConditions(
            station_id=data["station_id"],
            station_name=data["station_name"],
            time_zone=data["time_zone"],
            observed_at=datetime.fromisoformat(
                data["observed_at"]
            ),
            description=data["description"],
            temperature_f=data["temperature_f"],
            dewpoint_f=data["dewpoint_f"],
            humidity_percent=data["humidity_percent"],
            wind_direction_degrees=(
                data["wind_direction_degrees"]
            ),
            wind_direction_compass=(
                data["wind_direction_compass"]
            ),
            wind_speed_mph=data["wind_speed_mph"],
            wind_gust_mph=data["wind_gust_mph"],
            visibility_miles=data["visibility_miles"],
            pressure_inhg=data["pressure_inhg"],
            precipitation_last_hour_in=(
                data["precipitation_last_hour_in"]
            ),
            source=data["source"],
            raw_message=data["raw_message"],
        )

    def _deserialize_forecast(self, payload):
        data = json.loads(payload)

        return ForecastReport(
            region_code=data["region_code"],
            time_zone=data["time_zone"],
            generated_at=datetime.fromisoformat(
                data["generated_at"]
            ),
            period_name=data["period_name"],
            start_time=datetime.fromisoformat(
                data["start_time"]
            ),
            end_time=datetime.fromisoformat(
                data["end_time"]
            ),
            temperature=data["temperature"],
            temperature_unit=data["temperature_unit"],
            wind_direction=data["wind_direction"],
            wind_speed=data["wind_speed"],
            precipitation_chance=(
                data["precipitation_chance"]
            ),
            short_forecast=data["short_forecast"],
            detailed_forecast=data[
                "detailed_forecast"
            ],
            source=data["source"],
        )
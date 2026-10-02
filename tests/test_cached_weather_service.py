from datetime import datetime, timezone

import requests
import pytest

from models.current_conditions import CurrentConditions
from models.forecast_report import ForecastReport
from services.cached_weather_service import CachedWeatherService


def make_conditions():
    return CurrentConditions(
        station_id="PHNL",
        station_name="Daniel K Inouye International Airport",
        time_zone="Pacific/Honolulu",
        observed_at=datetime(
            2026,
            10,
            1,
            22,
            28,
            tzinfo=timezone.utc,
        ),
        description="Light Rain",
        temperature_f=77.0,
        dewpoint_f=73.9,
        humidity_percent=None,
        wind_direction_degrees=150,
        wind_direction_compass="SSE",
        wind_speed_mph=16.1,
        wind_gust_mph=None,
        visibility_miles=10.0,
        pressure_inhg=29.88,
        precipitation_last_hour_in=0.16,
        source="NWS",
        raw_message="PHNL test METAR",
    )


def make_forecast():
    return ForecastReport(
        region_code="96814",
        time_zone="Pacific/Honolulu",
        generated_at=datetime(
            2026,
            10,
            1,
            16,
            35,
            20,
            tzinfo=timezone.utc,
        ),
        period_name="Today",
        start_time=datetime(
            2026,
            10,
            1,
            16,
            0,
            tzinfo=timezone.utc,
        ),
        end_time=datetime(
            2026,
            10,
            2,
            4,
            0,
            tzinfo=timezone.utc,
        ),
        temperature=87,
        temperature_unit="F",
        wind_direction="SE",
        wind_speed="13 mph",
        precipitation_chance=63,
        short_forecast="Chance Rain Showers",
        detailed_forecast="A chance of rain showers.",
        source="NWS",
    )


class FakeCacheService:
    def __init__(
        self,
        current=None,
        stale_current=None,
        forecast=None,
        stale_forecast=None,
    ):
        self.current = current
        self.stale_current = stale_current
        self.forecast = forecast
        self.stale_forecast = stale_forecast
        self.saved_current = None
        self.saved_forecast = None

    def get_current(self, cache_key):
        return self.current

    def get_current_stale(self, cache_key):
        return self.stale_current

    def save_current(self, cache_key, conditions):
        self.saved_current = (
            cache_key,
            conditions,
        )

    def get_forecast(self, cache_key):
        return self.forecast

    def get_forecast_stale(self, cache_key):
        return self.stale_forecast

    def save_forecast(self, cache_key, forecast):
        self.saved_forecast = (
            cache_key,
            forecast,
        )


class FakeNwsWeatherService:
    def __init__(
        self,
        conditions=None,
        forecast=None,
        current_error=None,
        forecast_error=None,
    ):
        self.conditions = conditions
        self.forecast = forecast
        self.current_error = current_error
        self.forecast_error = forecast_error
        self.current_call_count = 0
        self.forecast_call_count = 0

    def get_current_conditions(self, location):
        self.current_call_count += 1

        if self.current_error is not None:
            raise self.current_error

        return self.conditions

    def get_forecast(self, location, region_code):
        self.forecast_call_count += 1

        if self.forecast_error is not None:
            raise self.forecast_error

        return self.forecast


def test_current_cache_hit_does_not_call_nws():
    conditions = make_conditions()

    cache = FakeCacheService(
        current=conditions,
    )

    nws = FakeNwsWeatherService(
        conditions=conditions,
    )

    service = CachedWeatherService(
        nws_weather_service=nws,
        cache_service=cache,
    )

    result = service.get_current_conditions(
        location=object(),
        cache_key="CURRENT:ZIP:96814",
    )

    assert result.data == conditions
    assert result.is_stale is False
    assert nws.current_call_count == 0
    assert cache.saved_current is None


def test_current_cache_miss_fetches_and_saves():
    conditions = make_conditions()

    cache = FakeCacheService()

    nws = FakeNwsWeatherService(
        conditions=conditions,
    )

    service = CachedWeatherService(
        nws_weather_service=nws,
        cache_service=cache,
    )

    result = service.get_current_conditions(
        location=object(),
        cache_key="CURRENT:ZIP:96814",
    )

    assert result.data == conditions
    assert result.is_stale is False
    assert nws.current_call_count == 1

    assert cache.saved_current == (
        "CURRENT:ZIP:96814",
        conditions,
    )


def test_current_nws_failure_returns_stale_cache():
    conditions = make_conditions()

    cache = FakeCacheService(
        stale_current=conditions,
    )

    nws = FakeNwsWeatherService(
        current_error=requests.ConnectionError(
            "NWS unavailable"
        ),
    )

    service = CachedWeatherService(
        nws_weather_service=nws,
        cache_service=cache,
    )

    result = service.get_current_conditions(
        location=object(),
        cache_key="CURRENT:ZIP:96814",
    )

    assert result.data == conditions
    assert result.is_stale is True
    assert nws.current_call_count == 1
    assert cache.saved_current is None


def test_forecast_cache_hit_does_not_call_nws():
    forecast = make_forecast()

    cache = FakeCacheService(
        forecast=forecast,
    )

    nws = FakeNwsWeatherService(
        forecast=forecast,
    )

    service = CachedWeatherService(
        nws_weather_service=nws,
        cache_service=cache,
    )

    result = service.get_forecast(
        location=object(),
        region_code="96814",
        cache_key="FORECAST:ZIP:96814",
    )

    assert result.data == forecast
    assert result.is_stale is False
    assert nws.forecast_call_count == 0
    assert cache.saved_forecast is None


def test_forecast_cache_miss_fetches_and_saves():
    forecast = make_forecast()

    cache = FakeCacheService()

    nws = FakeNwsWeatherService(
        forecast=forecast,
    )

    service = CachedWeatherService(
        nws_weather_service=nws,
        cache_service=cache,
    )

    result = service.get_forecast(
        location=object(),
        region_code="96814",
        cache_key="FORECAST:ZIP:96814",
    )

    assert result.data == forecast
    assert result.is_stale is False
    assert nws.forecast_call_count == 1

    assert cache.saved_forecast == (
        "FORECAST:ZIP:96814",
        forecast,
    )


def test_forecast_nws_failure_returns_stale_cache():
    forecast = make_forecast()

    cache = FakeCacheService(
        stale_forecast=forecast,
    )

    nws = FakeNwsWeatherService(
        forecast_error=requests.ConnectionError(
            "NWS unavailable"
        ),
    )

    service = CachedWeatherService(
        nws_weather_service=nws,
        cache_service=cache,
    )

    result = service.get_forecast(
        location=object(),
        region_code="96814",
        cache_key="FORECAST:ZIP:96814",
    )

    assert result.data == forecast
    assert result.is_stale is True
    assert nws.forecast_call_count == 1
    assert cache.saved_forecast is None

def test_current_nws_failure_without_stale_cache_raises():
    cache = FakeCacheService()

    nws = FakeNwsWeatherService(
        current_error=requests.ConnectionError(
            "NWS unavailable"
        ),
    )

    service = CachedWeatherService(
        nws_weather_service=nws,
        cache_service=cache,
    )

    with pytest.raises(requests.ConnectionError):
        service.get_current_conditions(
            location=object(),
            cache_key="CURRENT:ZIP:96814",
        )

    assert nws.current_call_count == 1


def test_forecast_nws_failure_without_stale_cache_raises():
    cache = FakeCacheService()

    nws = FakeNwsWeatherService(
        forecast_error=requests.ConnectionError(
            "NWS unavailable"
        ),
    )

    service = CachedWeatherService(
        nws_weather_service=nws,
        cache_service=cache,
    )

    with pytest.raises(requests.ConnectionError):
        service.get_forecast(
            location=object(),
            region_code="96814",
            cache_key="FORECAST:ZIP:96814",
        )

    assert nws.forecast_call_count == 1
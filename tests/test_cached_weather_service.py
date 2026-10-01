from datetime import datetime, timezone

from models.current_conditions import CurrentConditions
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


class FakeCacheService:
    def __init__(self, cached=None):
        self.cached = cached
        self.saved = None

    def get_current(self, cache_key):
        return self.cached

    def save_current(self, cache_key, conditions):
        self.saved = (cache_key, conditions)


class FakeNwsWeatherService:
    def __init__(self, conditions):
        self.conditions = conditions
        self.call_count = 0

    def get_current_conditions(self, location):
        self.call_count += 1
        return self.conditions


def test_current_cache_hit_does_not_call_nws():
    conditions = make_conditions()

    cache = FakeCacheService(
        cached=conditions
    )

    nws = FakeNwsWeatherService(
        conditions
    )

    service = CachedWeatherService(
        nws_weather_service=nws,
        cache_service=cache,
    )

    result = service.get_current_conditions(
        location=object(),
        cache_key="CURRENT:ZIP:96814",
    )

    assert result == conditions
    assert nws.call_count == 0


def test_current_cache_miss_fetches_and_saves():
    conditions = make_conditions()

    cache = FakeCacheService()

    nws = FakeNwsWeatherService(
        conditions
    )

    service = CachedWeatherService(
        nws_weather_service=nws,
        cache_service=cache,
    )

    location = object()

    result = service.get_current_conditions(
        location=location,
        cache_key="CURRENT:ZIP:96814",
    )

    assert result == conditions
    assert nws.call_count == 1

    assert cache.saved == (
        "CURRENT:ZIP:96814",
        conditions,
    )
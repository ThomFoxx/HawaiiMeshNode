from services.weather_refresh_service import (
    WeatherRefreshService,
)


class FakeZipRequestRepository:
    def get_recently_requested(
        self,
        cutoff,
        limit,
    ):
        return [
            "96814",
            "96815",
        ]


class FakeZipLocationService:
    def find(self, zip_code):
        return f"LOCATION:{zip_code}"


class FakeCachedWeatherService:
    def __init__(self):
        self.current_calls = []
        self.forecast_calls = []

    def get_current_conditions(
        self,
        location,
        cache_key,
    ):
        self.current_calls.append(
            (
                location,
                cache_key,
            )
        )

    def get_forecast(
        self,
        location,
        region_code,
        cache_key,
    ):
        self.forecast_calls.append(
            (
                location,
                region_code,
                cache_key,
            )
        )


class FakeCacheService:
    def __init__(self):
        self.cleanup_count = 0

    def cleanup(self):
        self.cleanup_count += 1


def test_refresh_once_refreshes_recent_zips():
    zip_requests = FakeZipRequestRepository()
    locations = FakeZipLocationService()
    weather = FakeCachedWeatherService()
    cache = FakeCacheService()

    service = WeatherRefreshService(
        zip_request_repository=zip_requests,
        zip_location_service=locations,
        cached_weather_service=weather,
        cache_service=cache,
    )

    service.refresh_once()

    assert cache.cleanup_count == 1

    assert (
        "LOCATION:96814",
        "CURRENT:REGION:OAHU",
    ) in weather.current_calls

    assert (
        "LOCATION:96732",
        "CURRENT:REGION:MAUI",
    ) in weather.current_calls

    assert (
        "LOCATION:96766",
        "CURRENT:REGION:KAUAI",
    ) in weather.current_calls

    assert (
        "LOCATION:96720",
        "CURRENT:REGION:HAWAII",
    ) in weather.current_calls

    assert (
        "LOCATION:96814",
        "CURRENT:ZIP:96814",
    ) in weather.current_calls

    assert (
        "LOCATION:96815",
        "CURRENT:ZIP:96815",
    ) in weather.current_calls

    assert (
        "LOCATION:96814",
        "OAHU",
        "FORECAST:REGION:OAHU",
    ) in weather.forecast_calls

    assert (
        "LOCATION:96732",
        "MAUI",
        "FORECAST:REGION:MAUI",
    ) in weather.forecast_calls

    assert (
        "LOCATION:96766",
        "KAUAI",
        "FORECAST:REGION:KAUAI",
    ) in weather.forecast_calls

    assert (
        "LOCATION:96720",
        "HAWAII",
        "FORECAST:REGION:HAWAII",
    ) in weather.forecast_calls

    assert (
        "LOCATION:96814",
        "96814",
        "FORECAST:ZIP:96814",
    ) in weather.forecast_calls

    assert (
        "LOCATION:96815",
        "96815",
        "FORECAST:ZIP:96815",
    ) in weather.forecast_calls
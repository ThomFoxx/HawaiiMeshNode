import threading
from datetime import datetime, timedelta, timezone

import requests

from data.zip_request_repository import ZipRequestRepository
from services.cached_weather_service import CachedWeatherService
from services.weather_cache_service import WeatherCacheService
from services.zip_location_service import ZipLocationService
from data.weather_regions import WEATHER_REGIONS


REFRESH_INTERVAL = timedelta(minutes=10)
ACTIVE_ZIP_WINDOW = timedelta(hours=24)
MAX_ACTIVE_ZIPS = 5


class WeatherRefreshService:
    def __init__(
        self,
        zip_request_repository=None,
        zip_location_service=None,
        cached_weather_service=None,
        cache_service=None,
    ):
        self.zip_request_repository = (
            zip_request_repository
            if zip_request_repository is not None
            else ZipRequestRepository()
        )

        self.zip_location_service = (
            zip_location_service
            if zip_location_service is not None
            else ZipLocationService()
        )

        self.cached_weather_service = (
            cached_weather_service
            if cached_weather_service is not None
            else CachedWeatherService()
        )

        self.cache_service = (
            cache_service
            if cache_service is not None
            else WeatherCacheService()
        )

        self._stop_event = threading.Event()
        self._thread = None

    def start(self):
        if self._thread is not None:
            return

        self._thread = threading.Thread(
            target=self._run,
            name="weather-refresh",
            daemon=True,
        )

        self._thread.start()

    def stop(self):
        self._stop_event.set()

        if self._thread is not None:
            self._thread.join(timeout=5)

        self._thread = None

    def refresh_once(self):
        self.cache_service.cleanup()

        self._refresh_regions()
        self._refresh_recent_zips()

    def _refresh_regions(self):
        for region in WEATHER_REGIONS:
            location = self.zip_location_service.find(
                region.weather_zip
            )

            if location is None:
                continue

            self._refresh_region_current(
                region,
                location,
            )

            self._refresh_region_forecast(
                region,
                location,
            )

    def _refresh_recent_zips(self):
        cutoff = (
            datetime.now(timezone.utc)
            - ACTIVE_ZIP_WINDOW
        )

        zip_codes = (
            self.zip_request_repository
            .get_recently_requested(
                cutoff,
                MAX_ACTIVE_ZIPS,
            )
        )

        for zip_code in zip_codes:
            location = self.zip_location_service.find(
                zip_code
            )

            if location is None:
                continue

            self._refresh_current(
                zip_code,
                location,
            )

            self._refresh_forecast(
                zip_code,
                location,
            )

    def _refresh_current(
        self,
        zip_code,
        location,
    ):
        cache_key = f"CURRENT:ZIP:{zip_code}"

        try:
            self.cached_weather_service.get_current_conditions(
                location,
                cache_key,
            )

        except (
            requests.RequestException,
            RuntimeError,
        ):
            pass

    def _refresh_forecast(
        self,
        zip_code,
        location,
    ):
        cache_key = f"FORECAST:ZIP:{zip_code}"

        try:
            self.cached_weather_service.get_forecast(
                location,
                zip_code,
                cache_key,
            )

        except (
            requests.RequestException,
            RuntimeError,
        ):
            pass

    def _run(self):
        while not self._stop_event.is_set():
            self.refresh_once()

            self._stop_event.wait(
                REFRESH_INTERVAL.total_seconds()
            )

    def _refresh_region_current(
        self,
        region,
        location,
    ):
        cache_key = (
            f"CURRENT:REGION:{region.code}"
        )

        try:
            self.cached_weather_service.get_current_conditions(
                location,
                cache_key,
            )

        except (
            requests.RequestException,
            RuntimeError,
        ):
            pass

    def _refresh_region_forecast(
        self,
        region,
        location,
    ):
        cache_key = (
            f"FORECAST:REGION:{region.code}"
        )

        try:
            self.cached_weather_service.get_forecast(
                location,
                region.code,
                cache_key,
            )

        except (
            requests.RequestException,
            RuntimeError,
        ):
            pass
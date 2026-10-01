from services.nws_weather_service import NwsWeatherService
from services.weather_cache_service import WeatherCacheService


class CachedWeatherService:
    def __init__(
        self,
        nws_weather_service=None,
        cache_service=None,
    ):
        self.nws_weather_service = (
            nws_weather_service
            if nws_weather_service is not None
            else NwsWeatherService()
        )

        self.cache_service = (
            cache_service
            if cache_service is not None
            else WeatherCacheService()
        )

    def get_current_conditions(
        self,
        location,
        cache_key,
    ):
        cached = self.cache_service.get_current(
            cache_key
        )

        if cached is not None:
            return cached

        conditions = (
            self.nws_weather_service
            .get_current_conditions(location)
        )

        self.cache_service.save_current(
            cache_key,
            conditions,
        )

        return conditions

    def get_forecast(
        self,
        location,
        region_code,
        cache_key,
    ):
        cached = self.cache_service.get_forecast(
            cache_key
        )

        if cached is not None:
            return cached

        forecast = (
            self.nws_weather_service.get_forecast(
                location,
                region_code,
            )
        )

        self.cache_service.save_forecast(
            cache_key,
            forecast,
        )

        return forecast
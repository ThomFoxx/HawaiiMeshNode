from models.weather_report import WeatherReport


class WeatherService:
    def get_weather(self, region):
        return WeatherReport(
            region_code=region.code,
            region_name=region.name,
            summary="Placeholder weather data.",
        )
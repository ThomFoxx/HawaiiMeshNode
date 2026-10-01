from models.weather_report import WeatherReport


class WeatherService:
    def get_current_conditions(self, region):
        return WeatherReport(
            region_code=region.code,
            region_name=region.name,
            summary="Placeholder current conditions.",
        )

    def get_forecast(self, region):
        return WeatherReport(
            region_code=region.code,
            region_name=region.name,
            summary="Placeholder forecast.",
        )

    def get_current_conditions_by_zip(self, zip_code):
        return WeatherReport(
            region_code=zip_code,
            region_name=f"ZIP {zip_code}",
            summary="Placeholder current conditions.",
        )

    def get_forecast_by_zip(self, zip_code):
        return WeatherReport(
            region_code=zip_code,
            region_name=f"ZIP {zip_code}",
            summary="Placeholder forecast.",
        )
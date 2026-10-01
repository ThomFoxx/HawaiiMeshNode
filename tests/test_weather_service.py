from models.region import Region
from services.weather_service import WeatherService


def test_get_weather_returns_report():
    service = WeatherService()
    region = Region("OAHU", "Oahu")

    report = service.get_weather(region)

    assert report.region_code == "OAHU"
    assert report.region_name == "Oahu"
    assert report.summary == "Placeholder weather data."
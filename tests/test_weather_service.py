from models.region import Region
from services.weather_service import WeatherService


def test_get_current_conditions():
    service = WeatherService()
    region = Region("OAHU", "Oahu")

    report = service.get_current_conditions(region)

    assert report.region_code == "OAHU"
    assert report.region_name == "Oahu"
    assert report.summary == "Placeholder current conditions."


def test_get_forecast():
    service = WeatherService()
    region = Region("OAHU", "Oahu")

    report = service.get_forecast(region)

    assert report.region_code == "OAHU"
    assert report.region_name == "Oahu"
    assert report.summary == "Placeholder forecast."
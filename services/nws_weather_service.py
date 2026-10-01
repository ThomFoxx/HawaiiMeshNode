from services.current_conditions_service import CurrentConditionsService
from services.nws_client import NwsClient
from datetime import datetime
from models.forecast_report import ForecastReport


class NwsWeatherService:
    def __init__(self):
        self.client = NwsClient()
        self.conditions_service = CurrentConditionsService()

    def get_current_conditions(self, location):               
        point_data = self.client.get_point(
            location.latitude,
            location.longitude,
        )

        point = point_data["properties"]

        stations_data = self.client.get_json(
            point["observationStations"]
        )

        stations = stations_data.get("features", [])

        if len(stations) == 0:
            raise RuntimeError("No NWS observation stations found.")

        station = stations[0]
        station_properties = station["properties"]

        observation_url = (
            f"{station['id']}/observations/latest"
        )

        observation_data = self.client.get_json(
            observation_url
        )

        observation = observation_data["properties"]

        return self.conditions_service.build(
            station_id=station_properties.get(
                "stationIdentifier"
            ),
            station_name=station_properties.get("name"),
            time_zone=point["timeZone"],
            observation=observation,
        )

    def get_forecast(self, location, region_code):
        point_data = self.client.get_point(
            location.latitude,
            location.longitude,
        )

        point = point_data["properties"]

        forecast_data = self.client.get_json(
            point["forecast"]
        )

        forecast = forecast_data["properties"]
        periods = forecast.get("periods", [])

        if len(periods) == 0:
            raise RuntimeError("No NWS forecast periods found.")

        period = periods[0]

        precipitation = period.get(
            "probabilityOfPrecipitation",
            {},
        )

        return ForecastReport(
            region_code=region_code,
            time_zone=point["timeZone"],
            generated_at=datetime.fromisoformat(
                forecast["generatedAt"].replace(
                    "Z",
                    "+00:00",
                )
            ),
            period_name=period["name"],
            start_time=datetime.fromisoformat(
                period["startTime"]
            ),
            end_time=datetime.fromisoformat(
                period["endTime"]
            ),
            temperature=period.get("temperature"),
            temperature_unit=period.get(
                "temperatureUnit"
            ),
            wind_direction=period.get(
                "windDirection"
            ),
            wind_speed=period.get("windSpeed"),
            precipitation_chance=(
                precipitation.get("value")
            ),
            short_forecast=period.get(
                "shortForecast"
            ),
            detailed_forecast=period.get(
                "detailedForecast"
            ),
            source="NWS",
        )
    
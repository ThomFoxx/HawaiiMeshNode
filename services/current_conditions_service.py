from datetime import datetime

from models.current_conditions import CurrentConditions
from services.metar_service import MetarService


class CurrentConditionsService:
    def __init__(self):
        self.metar_service = MetarService()

    def build(
        self,
        station_id,
        station_name,
        time_zone,
        observation,
    ):
        raw_message = observation.get("rawMessage")
        metar = self.metar_service.parse(raw_message)

        observed_at = datetime.fromisoformat(
            observation["timestamp"].replace("Z", "+00:00")
        )

        temperature_f = self._get_temperature_f(
            observation,
            metar,
        )

        dewpoint_f = self._get_dewpoint_f(
            observation,
            metar,
        )

        humidity_percent = self._get_value(
            observation.get("relativeHumidity")
        )

        wind_direction_degrees = self._get_value(
            observation.get("windDirection")
        )

        if wind_direction_degrees is None:
            wind_direction_degrees = (
                self.metar_service.wind_direction_degrees(
                    metar
                )
            )

        wind_direction_compass = (
            self.metar_service.wind_direction_compass(
                metar
            )
        )

        wind_speed_mph = self._get_wind_speed_mph(
            observation,
            metar,
        )

        wind_gust_mph = self._get_wind_gust_mph(
            observation,
            metar,
        )

        visibility_miles = (
            self.metar_service.visibility_miles(
                metar
            )
        )

        pressure_inhg = (
            self.metar_service.pressure_inhg(
                metar
            )
        )

        precipitation_last_hour_in = (
            self.metar_service.precipitation_last_hour_in(
                metar
            )
        )

        return CurrentConditions(
            station_id=station_id,
            station_name=station_name,
            time_zone=time_zone,
            observed_at=observed_at,
            description=observation.get("textDescription"),
            temperature_f=temperature_f,
            dewpoint_f=dewpoint_f,
            humidity_percent=humidity_percent,
            wind_direction_degrees=wind_direction_degrees,
            wind_direction_compass=wind_direction_compass,
            wind_speed_mph=wind_speed_mph,
            wind_gust_mph=wind_gust_mph,
            visibility_miles=visibility_miles,
            pressure_inhg=pressure_inhg,
            precipitation_last_hour_in=precipitation_last_hour_in,
            source="NWS",
            raw_message=raw_message,
        )

    def _get_value(self, measurement):
        if measurement is None:
            return None

        return measurement.get("value")

    def _get_temperature_f(
        self,
        observation,
        metar,
    ):
        value = self._get_value(
            observation.get("temperature")
        )

        if value is not None:
            return (value * 9 / 5) + 32

        return self.metar_service.temperature_f(
            metar
        )

    def _get_dewpoint_f(
        self,
        observation,
        metar,
    ):
        value = self._get_value(
            observation.get("dewpoint")
        )

        if value is not None:
            return (value * 9 / 5) + 32

        return self.metar_service.dewpoint_f(
            metar
        )

    def _get_wind_speed_mph(
        self,
        observation,
        metar,
    ):
        value = self._get_value(
            observation.get("windSpeed")
        )

        if value is not None:
            return value * 0.621371

        return self.metar_service.wind_speed_mph(
            metar
        )

    def _get_wind_gust_mph(
        self,
        observation,
        metar,
    ):
        value = self._get_value(
            observation.get("windGust")
        )

        if value is not None:
            return value * 0.621371

        return self.metar_service.wind_gust_mph(
            metar
        )
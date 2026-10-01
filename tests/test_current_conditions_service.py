from services.current_conditions_service import (
    CurrentConditionsService,
)


def test_build_uses_metar_fallback():
    service = CurrentConditionsService()

    observation = {
        "timestamp": "2026-10-01T22:28:00+00:00",
        "textDescription": "Light Rain",
        "temperature": {
            "value": None,
        },
        "dewpoint": {
            "value": None,
        },
        "relativeHumidity": {
            "value": None,
        },
        "windDirection": {
            "value": None,
        },
        "windSpeed": {
            "value": None,
        },
        "windGust": {
            "value": None,
        },
        "rawMessage": (
            "PHNL 012228Z 15014KT 10SM -RA "
            "FEW022 BKN038 OVC055 25/23 A2988 "
            "RMK AO2 RAB06 P0016 "
            "T02500233 $"
        ),
    }

    conditions = service.build(
        station_id="PHNL",
        station_name=(
            "Daniel K Inouye International Airport"
        ),
        time_zone="Pacific/Honolulu",
        observation=observation,
    )

    assert conditions.station_id == "PHNL"
    assert conditions.temperature_f == 77.0
    assert round(conditions.wind_speed_mph, 1) == 16.1
    assert conditions.wind_direction_compass == "SSE"
    assert conditions.pressure_inhg == 29.88
    assert conditions.precipitation_last_hour_in == 0.16
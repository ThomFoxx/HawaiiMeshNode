from datetime import datetime, timezone
from zoneinfo import ZoneInfo

from services.nws_client import NwsClient


LATITUDE = 21.291214
LONGITUDE = -157.844002

HAWAII_TIME = ZoneInfo("Pacific/Honolulu")


def format_time(value):
    if value is None:
        return "Not provided"

    parsed = datetime.fromisoformat(
        value.replace("Z", "+00:00")
    )

    local = parsed.astimezone(HAWAII_TIME)

    return local.strftime("%Y-%m-%d %I:%M:%S %p HST")


def print_measurement(name, measurement):
    if measurement is None:
        print(f"{name}: Not provided")
        return

    value = measurement.get("value")
    unit = measurement.get("unitCode")

    print(f"{name}: {value} ({unit})")


def main():
    client = NwsClient()

    retrieved_at = datetime.now(timezone.utc)

    point_data = client.get_point(
        LATITUDE,
        LONGITUDE,
    )

    point = point_data["properties"]

    print("=== POINT ===")
    print(f"Grid: {point['gridId']} {point['gridX']},{point['gridY']}")
    print(f"Time zone: {point['timeZone']}")

    print()
    print("=== FORECAST ===")

    forecast_data = client.get_json(point["forecast"])
    forecast = forecast_data["properties"]

    print(
        "Generated:",
        format_time(forecast.get("generatedAt")),
    )

    print(
        "Updated:",
        format_time(forecast.get("updateTime")),
    )

    periods = forecast.get("periods", [])

    if periods:
        first_period = periods[0]

        print(f"Period: {first_period['name']}")

        print(
            f"Temperature: "
            f"{first_period.get('temperature')} "
            f"{first_period.get('temperatureUnit')}"
        )

        print(
            f"Wind: "
            f"{first_period.get('windDirection')} "
            f"{first_period.get('windSpeed')}"
        )

        precipitation = first_period.get(
            "probabilityOfPrecipitation",
            {},
        )

        print(
            "Precipitation chance:",
            precipitation.get("value"),
        )

        print(
            "Detailed forecast:",
            first_period.get("detailedForecast"),
        )

        print(
            "Starts:",
            format_time(first_period.get("startTime")),
        )

        print(
            "Ends:",
            format_time(first_period.get("endTime")),
        )

        print(
            "Forecast:",
            first_period.get("shortForecast"),
        )

    print()
    print("=== OBSERVATION STATION ===")

    stations_data = client.get_json(
        point["observationStations"]
    )

    stations = stations_data.get("features", [])

    if len(stations) == 0:
        print("No observation stations returned.")
        return

    station = stations[0]
    station_properties = station["properties"]
    station_url = station["id"]

    print(
        f"Station: "
        f"{station_properties.get('stationIdentifier')}"
    )

    print(
        f"Name: "
        f"{station_properties.get('name')}"
    )

    observations_data = client.get_recent_observations(
        station_url,
        limit=5,
    )

    observations = observations_data.get("features", [])

    print()
    print("=== RECENT OBSERVATIONS ===")

    if len(observations) == 0:
        print("No recent observations returned.")
        return

    for feature in observations:
        observation = feature["properties"]

        print()
        print(
            "Observed:",
            format_time(observation.get("timestamp")),
        )

        print(
            "Description:",
            observation.get("textDescription"),
        )

        print(
            "Raw:",
            observation.get("rawMessage"),
        )

        print_measurement(
            "Temperature",
            observation.get("temperature"),
        )

        print_measurement(
            "Dewpoint",
            observation.get("dewpoint"),
        )

        print_measurement(
            "Humidity",
            observation.get("relativeHumidity"),
        )

        print_measurement(
            "Wind direction",
            observation.get("windDirection"),
        )

        print_measurement(
            "Wind speed",
            observation.get("windSpeed"),
        )

        print_measurement(
            "Wind gust",
            observation.get("windGust"),
        )

        print_measurement(
            "Visibility",
            observation.get("visibility"),
        )

        print_measurement(
            "Barometric pressure",
            observation.get("barometricPressure"),
        )

        print_measurement(
            "Precip last hour",
            observation.get("precipitationLastHour"),
        )

    print()
    print("=== OUR CACHE METADATA ===")

    print(
        "Retrieved:",
        retrieved_at
        .astimezone(HAWAII_TIME)
        .strftime("%Y-%m-%d %I:%M:%S %p HST"),
    )


if __name__ == "__main__":
    main()
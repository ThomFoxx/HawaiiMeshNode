from models.region import Region
from services.weather_service import WeatherService
from data.zip_request_repository import ZipRequestRepository
from services.zip_location_service import ZipLocationService
from zoneinfo import ZoneInfo
from services.nws_weather_service import NwsWeatherService
from services.cached_weather_service import CachedWeatherService


WEATHER_REGIONS = {
    "OAHU": Region(
        "OAHU",
        "Oahu",
        ("OʻAHU", "O'AHU"),
    ),
    "MAUI": Region(
        "MAUI",
        "Maui",
    ),
    "KAUAI": Region(
        "KAUAI",
        "Kauai",
        ("KAUAʻI", "KAUA'I"),
    ),
    "HAWAII": Region(
        "HAWAII",
        "Hawaii Island",
        ("BIGISLAND", "BIG-ISLAND"),
    ),
}


weather_service = WeatherService()
zip_request_repository = ZipRequestRepository()
zip_request_repository.initialize()
zip_location_service = ZipLocationService()
nws_weather_service = NwsWeatherService()
cached_weather_service = CachedWeatherService()


def find_region(region_code):
    region = WEATHER_REGIONS.get(region_code)

    if region is not None:
        return region

    for candidate in WEATHER_REGIONS.values():
        if region_code in candidate.aliases:
            return candidate

    return None

def show_weather(arguments):
    if len(arguments) == 0:
        show_weather_help()
        return

    if arguments[0] == "ZIP":
        show_zip_weather(arguments[1:])
        return

    region_code = arguments[0]
    region = find_region(region_code)

    if region is None:
        print(f"Weather region not found: {region_code}")
        show_supported_regions()
        return

    mode = "CURRENT"

    if len(arguments) > 1:
        mode = arguments[1]

    if mode == "CURRENT":
        report = weather_service.get_current_conditions(region)
    elif mode == "FORECAST":
        report = weather_service.get_forecast(region)
    else:
        print(f"Unknown weather mode: {mode}")
        print("Available modes: CURRENT, FORECAST")
        return

    print(f"{report.region_name} weather: {report.summary}")

def show_weather_help():
    print("Weather regions:")
    show_supported_regions()

    print()
    print("Usage:")
    print("  WX <region>")
    print("  WX <region> CURRENT")
    print("  WX <region> FORECAST")
    print("  WX ZIP <zipcode>")
    print("  WX ZIP <zipcode> CURRENT")
    print("  WX ZIP <zipcode> FORECAST")

def show_supported_regions():
    for region in WEATHER_REGIONS.values():
        print(f"  {region.code:<7} - {region.name}")

def is_valid_zip_code(zip_code):
    return len(zip_code) == 5 and zip_code.isdigit()

def show_zip_weather(arguments):
    if len(arguments) == 0:
        print("Usage:")
        print("  WX ZIP <zipcode>")
        print("  WX ZIP <zipcode> CURRENT")
        print("  WX ZIP <zipcode> FORECAST")
        return

    zip_code = arguments[0]

    if not is_valid_zip_code(zip_code):
        print(f"Invalid ZIP code: {zip_code}")
        return

    location = zip_location_service.find(zip_code)

    if location is None:
        print(
            f"ZIP code not found in local catalog: "
            f"{zip_code}"
        )
        return

    zip_request_repository.record_request(zip_code)

    mode = "CURRENT"

    if len(arguments) > 1:
        mode = arguments[1]

    if mode == "CURRENT":
        cache_key = f"CURRENT:ZIP:{zip_code}"

        conditions = (
            cached_weather_service.get_current_conditions(
                location,
                cache_key,
            )
        )

        print(
            format_current_conditions(
                zip_code,
                conditions,
            )
        )

    elif mode == "FORECAST":
        cache_key = f"FORECAST:ZIP:{zip_code}"

        forecast = (
            cached_weather_service.get_forecast(
                location,
                zip_code,
                cache_key,
            )
        )

        print(
            format_forecast(
                zip_code,
                forecast,
            )
        )

    else:
        print(f"Unknown weather mode: {mode}")
        print("Available modes: CURRENT, FORECAST")

def format_current_conditions(zip_code, conditions):
    local_time = conditions.observed_at.astimezone(
        ZoneInfo(conditions.time_zone)
    )

    time_text = local_time.strftime(
        "%I:%M %p %Z"
    ).lstrip("0")

    parts = [
        f"ZIP {zip_code}:",
        conditions.description or "Conditions unavailable",
    ]

    if conditions.temperature_f is not None:
        parts.append(
            f"{round(conditions.temperature_f)}F"
        )

    if conditions.wind_direction_compass is not None:
        wind = conditions.wind_direction_compass

        if conditions.wind_speed_mph is not None:
            wind += (
                f" {round(conditions.wind_speed_mph)} mph"
            )

        parts.append(wind)

    parts.append(f"Obs {time_text}")
    parts.append(
        f"{conditions.station_id}/NWS"
    )

    return " ".join(parts)

def format_forecast(zip_code, forecast):
    local_time = forecast.generated_at.astimezone(
        ZoneInfo(forecast.time_zone)
    )

    generated_text = local_time.strftime(
        "%I:%M %p %Z"
    ).lstrip("0")

    parts = [
        f"ZIP {zip_code}:",
        forecast.period_name,
    ]

    if forecast.short_forecast is not None:
        parts.append(forecast.short_forecast)

    if forecast.temperature is not None:
        parts.append(
            f"{forecast.temperature}"
            f"{forecast.temperature_unit}"
        )

    if forecast.wind_direction is not None:
        wind = forecast.wind_direction

        if forecast.wind_speed is not None:
            wind += f" {forecast.wind_speed}"

        parts.append(wind)

    if forecast.precipitation_chance is not None:
        parts.append(
            f"Rain {forecast.precipitation_chance}%"
        )

    parts.append(f"Gen {generated_text}")
    parts.append("NWS")

    return " ".join(parts)

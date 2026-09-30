WEATHER_REGIONS = {
    "OAHU": "Oahu",
    "MAUI": "Maui",
    "KAUAI": "Kauai",
    "HAWAII": "Hawaii Island",
}


def show_weather(arguments):
    if len(arguments) == 0:
        print("Weather regions:")

        for code, name in WEATHER_REGIONS.items():
            print(f"  {code:<7} - {name}")

        print()
        print("Usage: WX <region>")
        return

    region = arguments[0]

    region_name = WEATHER_REGIONS.get(region)

    if region_name is None:
        print(f"Weather region not found: {region}")
        print("Supported regions:")

        for code, name in WEATHER_REGIONS.items():
            print(f"  {code:<7} - {name}")

        return

    print(f"{region_name} weather: placeholder data.")
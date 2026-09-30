from models.region import Region


WEATHER_REGIONS = {
    "OAHU": Region("OAHU", "Oahu"),
    "MAUI": Region("MAUI", "Maui"),
    "KAUAI": Region("KAUAI", "Kauai"),
    "HAWAII": Region("HAWAII", "Hawaii Island"),
}


def show_weather(arguments):
    if len(arguments) == 0:
        print("Weather regions:")

        for region in WEATHER_REGIONS.values():
            print(f"  {region.code:<7} - {region.name}")

        print()
        print("Usage: WX <region>")
        return

    region_code = arguments[0]
    region = WEATHER_REGIONS.get(region_code)

    if region is None:
        print(f"Weather region not found: {region_code}")
        print("Supported regions:")

        for supported_region in WEATHER_REGIONS.values():
            print(f"  {supported_region.code:<7} - {supported_region.name}")

        return

    print(f"{region.name} weather: placeholder data.")
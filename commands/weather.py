from models.region import Region


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
        print("Weather regions:")

        for region in WEATHER_REGIONS.values():
            print(f"  {region.code:<7} - {region.name}")

        print()
        print("Usage: WX <region>")
        return

    region_code = arguments[0]
    region = find_region(region_code)

    if region is None:
        print(f"Weather region not found: {region_code}")
        print("Supported regions:")

        for supported_region in WEATHER_REGIONS.values():
            print(
                f"  {supported_region.code:<7} - "
                f"{supported_region.name}"
            )

        return

    print(f"{region.name} weather: placeholder data.")
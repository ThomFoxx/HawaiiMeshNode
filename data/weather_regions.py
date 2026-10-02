from models.region import Region


WEATHER_REGIONS = (
    Region(
        code="OAHU",
        name="Oahu",
        weather_zip="96814",
        aliases=("OʻAHU", "O'AHU"),
    ),
    Region(
        code="MAUI",
        name="Maui",
        weather_zip="96732",
    ),
    Region(
        code="KAUAI",
        name="Kauai",
        weather_zip="96766",
        aliases=("KAUAʻI", "KAUA'I"),
    ),
    Region(
        code="HAWAII",
        name="Hawaii Island",
        weather_zip="96720",
        aliases=("BIGISLAND", "BIG-ISLAND"),
    ),
)


def find_region(region_code):
    normalized = region_code.upper()

    for region in WEATHER_REGIONS:
        if normalized == region.code:
            return region

        aliases = tuple(
            alias.upper()
            for alias in region.aliases
        )

        if normalized in aliases:
            return region

    return None
from commands.weather import find_region


def test_find_region_by_code():
    region = find_region("OAHU")

    assert region is not None
    assert region.code == "OAHU"
    assert region.name == "Oahu"


def test_find_region_by_alias():
    region = find_region("O'AHU")

    assert region is not None
    assert region.code == "OAHU"


def test_find_region_big_island_alias():
    region = find_region("BIGISLAND")

    assert region is not None
    assert region.code == "HAWAII"


def test_unknown_region_returns_none():
    region = find_region("MOON")

    assert region is None
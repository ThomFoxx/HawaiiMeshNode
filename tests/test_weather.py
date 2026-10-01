from commands.weather import find_region
from commands.weather import find_region, is_valid_zip_code


def test_valid_zip_code():
    assert is_valid_zip_code("96814")


def test_zip_code_must_be_five_digits():
    assert not is_valid_zip_code("9681")


def test_zip_code_must_be_numeric():
    assert not is_valid_zip_code("ABCDE")

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
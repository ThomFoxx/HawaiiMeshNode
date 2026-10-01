from datetime import datetime, timedelta, timezone

from data.weather_cache_repository import WeatherCacheRepository
from models.weather_cache_entry import WeatherCacheEntry


def test_save_and_get_weather_cache(tmp_path):
    db_path = tmp_path / "test.db"

    repository = WeatherCacheRepository(db_path)
    repository.initialize()

    now = datetime.now(timezone.utc)

    entry = WeatherCacheEntry(
        cache_key="CURRENT:ZIP:96814",
        data_type="CURRENT",
        payload='{"temperature_f": 77.0}',
        source_time=now,
        retrieved_at=now,
        expires_at=now + timedelta(minutes=10),
    )

    repository.save(entry)

    loaded = repository.get("CURRENT:ZIP:96814")

    assert loaded is not None
    assert loaded.cache_key == "CURRENT:ZIP:96814"
    assert loaded.data_type == "CURRENT"
    assert loaded.payload == '{"temperature_f": 77.0}'
    assert loaded.source_time == now
    assert loaded.retrieved_at == now


def test_save_updates_existing_weather_cache(tmp_path):
    db_path = tmp_path / "test.db"

    repository = WeatherCacheRepository(db_path)
    repository.initialize()

    now = datetime.now(timezone.utc)

    first = WeatherCacheEntry(
        cache_key="CURRENT:ZIP:96814",
        data_type="CURRENT",
        payload='{"temperature_f": 77.0}',
        source_time=now,
        retrieved_at=now,
        expires_at=now + timedelta(minutes=10),
    )

    updated = WeatherCacheEntry(
        cache_key="CURRENT:ZIP:96814",
        data_type="CURRENT",
        payload='{"temperature_f": 79.0}',
        source_time=now,
        retrieved_at=now,
        expires_at=now + timedelta(minutes=10),
    )

    repository.save(first)
    repository.save(updated)

    loaded = repository.get("CURRENT:ZIP:96814")

    assert loaded is not None
    assert loaded.payload == '{"temperature_f": 79.0}'


def test_weather_cache_entry_expiration():
    now = datetime.now(timezone.utc)

    entry = WeatherCacheEntry(
        cache_key="CURRENT:ZIP:96814",
        data_type="CURRENT",
        payload="{}",
        source_time=now,
        retrieved_at=now,
        expires_at=now + timedelta(minutes=10),
    )

    assert entry.is_expired(now) is False
    assert entry.is_expired(
        now + timedelta(minutes=11)
    ) is True
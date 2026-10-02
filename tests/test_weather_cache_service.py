from datetime import datetime, timedelta, timezone
from dataclasses import replace
from data.weather_cache_repository import WeatherCacheRepository
from models.current_conditions import CurrentConditions
from models.weather_cache_entry import WeatherCacheEntry
from models.forecast_report import ForecastReport
from services.weather_cache_service import WeatherCacheService


def make_conditions():
    return CurrentConditions(
        station_id="PHNL",
        station_name="Daniel K Inouye International Airport",
        time_zone="Pacific/Honolulu",
        observed_at=datetime(
            2026,
            10,
            1,
            22,
            28,
            tzinfo=timezone.utc,
        ),
        description="Light Rain",
        temperature_f=77.0,
        dewpoint_f=73.9,
        humidity_percent=None,
        wind_direction_degrees=150,
        wind_direction_compass="SSE",
        wind_speed_mph=16.1,
        wind_gust_mph=None,
        visibility_miles=10.0,
        pressure_inhg=29.88,
        precipitation_last_hour_in=0.16,
        source="NWS",
        raw_message=(
            "PHNL 012228Z 15014KT 10SM -RA "
            "FEW022 BKN038 OVC055 25/23 A2988"
        ),
    )


def test_save_and_get_current_conditions(tmp_path):
    repository = WeatherCacheRepository(
        tmp_path / "test.db"
    )

    service = WeatherCacheService(repository)

    conditions = make_conditions()

    service.save_current(
        "CURRENT:ZIP:96814",
        conditions,
    )

    loaded = service.get_current(
        "CURRENT:ZIP:96814"
    )

    assert loaded is not None
    assert loaded.station_id == "PHNL"
    assert loaded.temperature_f == 77.0
    assert loaded.wind_direction_compass == "SSE"
    assert loaded.observed_at == conditions.observed_at


def test_missing_current_cache_returns_none(tmp_path):
    repository = WeatherCacheRepository(
        tmp_path / "test.db"
    )

    service = WeatherCacheService(repository)

    loaded = service.get_current(
        "CURRENT:ZIP:96814"
    )

    assert loaded is None


def test_expired_current_cache_returns_none(tmp_path):
    repository = WeatherCacheRepository(
        tmp_path / "test.db"
    )

    service = WeatherCacheService(repository)

    now = datetime.now(timezone.utc)

    entry = WeatherCacheEntry(
        cache_key="CURRENT:ZIP:96814",
        data_type="CURRENT",
        payload="{}",
        source_time=now - timedelta(hours=1),
        retrieved_at=now - timedelta(hours=1),
        expires_at=now - timedelta(minutes=1),
    )

    repository.save(entry)

    loaded = service.get_current(
        "CURRENT:ZIP:96814"
    )

    assert loaded is None

def make_forecast():
    return ForecastReport(
        region_code="96814",
        time_zone="Pacific/Honolulu",
        generated_at=datetime(
            2026,
            10,
            1,
            16,
            35,
            20,
            tzinfo=timezone.utc,
        ),
        period_name="Today",
        start_time=datetime(
            2026,
            10,
            1,
            16,
            0,
            tzinfo=timezone.utc,
        ),
        end_time=datetime(
            2026,
            10,
            2,
            4,
            0,
            tzinfo=timezone.utc,
        ),
        temperature=87,
        temperature_unit="F",
        wind_direction="SE",
        wind_speed="13 mph",
        precipitation_chance=63,
        short_forecast="Chance Rain Showers",
        detailed_forecast=(
            "A chance of rain showers."
        ),
        source="NWS",
    )

def test_save_and_get_forecast(tmp_path):
    repository = WeatherCacheRepository(
        tmp_path / "test.db"
    )

    service = WeatherCacheService(repository)

    forecast = make_forecast()

    service.save_forecast(
        "FORECAST:ZIP:96814",
        forecast,
    )

    loaded = service.get_forecast(
        "FORECAST:ZIP:96814"
    )

    assert loaded is not None
    assert loaded.region_code == "96814"
    assert loaded.period_name == "Today"
    assert loaded.temperature == 87
    assert loaded.precipitation_chance == 63
    assert loaded.generated_at == forecast.generated_at

def test_expired_current_can_be_loaded_as_stale(tmp_path):
    repository = WeatherCacheRepository(
        tmp_path / "test.db"
    )

    service = WeatherCacheService(repository)

    now = datetime.now(timezone.utc)

    conditions = replace(
        make_conditions(),
        observed_at=now - timedelta(hours=1),
    )

    service.save_current(
        "CURRENT:ZIP:96814",
        conditions,
    )

    entry = repository.get(
        "CURRENT:ZIP:96814"
    )

    expired_entry = WeatherCacheEntry(
        cache_key=entry.cache_key,
        data_type=entry.data_type,
        payload=entry.payload,
        source_time=entry.source_time,
        retrieved_at=now - timedelta(hours=1),
        expires_at=now - timedelta(minutes=1),
    )

    repository.save(expired_entry)

    fresh = service.get_current(
        "CURRENT:ZIP:96814"
    )

    stale = service.get_current_stale(
        "CURRENT:ZIP:96814"
    )

    assert fresh is None
    assert stale is not None
    assert stale.station_id == "PHNL"
    assert stale.temperature_f == 77.0

def test_cleanup_removes_old_cache_entries(tmp_path):
    repository = WeatherCacheRepository(
        tmp_path / "test.db"
    )

    service = WeatherCacheService(repository)

    now = datetime.now(timezone.utc)

    old_entry = WeatherCacheEntry(
        cache_key="CURRENT:ZIP:11111",
        data_type="CURRENT",
        payload="{}",
        source_time=now - timedelta(days=10),
        retrieved_at=now - timedelta(days=10),
        expires_at=now - timedelta(days=10),
    )

    recent_entry = WeatherCacheEntry(
        cache_key="CURRENT:ZIP:22222",
        data_type="CURRENT",
        payload="{}",
        source_time=now,
        retrieved_at=now,
        expires_at=now + timedelta(minutes=10),
    )

    repository.save(old_entry)
    repository.save(recent_entry)

    deleted = service.cleanup()

    assert deleted == 1

    assert repository.get(
        "CURRENT:ZIP:11111"
    ) is None

    assert repository.get(
        "CURRENT:ZIP:22222"
    ) is not None


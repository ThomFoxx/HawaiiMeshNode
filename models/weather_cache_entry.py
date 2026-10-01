from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class WeatherCacheEntry:
    cache_key: str
    data_type: str
    payload: str
    source_time: datetime
    retrieved_at: datetime
    expires_at: datetime

    def is_expired(self, now):
        return now >= self.expires_at
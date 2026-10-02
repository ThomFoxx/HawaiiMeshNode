from dataclasses import dataclass


@dataclass(frozen=True)
class Region:
    code: str
    name: str
    weather_zip: str
    aliases: tuple[str, ...] = ()
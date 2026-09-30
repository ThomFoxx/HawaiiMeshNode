from dataclasses import dataclass


@dataclass(frozen=True)
class Region:
    code: str
    name: str
    aliases: tuple[str, ...] = ()
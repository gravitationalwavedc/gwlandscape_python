from dataclasses import dataclass


@dataclass(frozen=True)
class Keyword:
    id: str
    tag: str

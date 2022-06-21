from dataclasses import dataclass


@dataclass(frozen=True)
class Model:
    id: str
    name: str
    summary: str
    description: str

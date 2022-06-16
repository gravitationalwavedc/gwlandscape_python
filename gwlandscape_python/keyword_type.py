from dataclasses import dataclass


@dataclass(repr=True)
class Keyword:
    id: str
    tag: str

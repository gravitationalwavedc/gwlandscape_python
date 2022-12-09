from dataclasses import dataclass


@dataclass(frozen=True)
class Keyword:
    id: str
    tag: str

    def __repr__(self):
        return f'Keyword("{self.tag}")'

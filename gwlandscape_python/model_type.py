from dataclasses import dataclass


@dataclass(frozen=True)
class Model:
    id: str
    name: str
    summary: str
    description: str

    def __repr__(self):
        return f'Model("{self.name}")'

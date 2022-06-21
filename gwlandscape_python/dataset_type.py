from dataclasses import dataclass

from gwlandscape_python.model_type import Model
from gwlandscape_python.publication_type import Publication


@dataclass(frozen=True)
class Dataset:
    id: str
    publication: Publication
    model: Model
    files: list

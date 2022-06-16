from dataclasses import dataclass


@dataclass(repr=True)
class Keyword:
    id: str
    tag: str

    def __init__(self, keyword_data):
        self.tag = keyword_data['tag']
        self.id = keyword_data['id']

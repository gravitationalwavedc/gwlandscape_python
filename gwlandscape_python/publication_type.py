from dataclasses import dataclass


@dataclass(frozen=True)
class Publication:
    id: str
    author: str
    published: bool
    title: str
    year: int
    journal: str
    journal_doi: str
    dataset_doi: str
    description: str
    public: bool
    download_link: str
    arxiv_id: str
    creation_time: str
    keywords: list

    def __repr__(self):
        return f'Publication("{self.title}")'

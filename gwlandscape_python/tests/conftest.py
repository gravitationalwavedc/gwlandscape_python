import pytest
from gwlandscape_python import GWLandscape
from gwlandscape_python.dataset_type import Dataset
from gwlandscape_python.keyword_type import Keyword
from gwlandscape_python.model_type import Model
from gwlandscape_python.publication_type import Publication


@pytest.fixture
def setup_gwl_request(mocker):
    def mock_init(self, token, auth_endpoint, endpoint):
        pass

    mock_request = mocker.Mock()
    mocker.patch('gwlandscape_python.gwlandscape.GWDC.__init__', mock_init)
    mocker.patch('gwlandscape_python.gwlandscape.GWDC.request', mock_request)

    return GWLandscape(token='my_token'), mock_request

@pytest.fixture
def mock_keyword_data():
    def _mock_keyword_data(i=1):
        return {'tag': f'mock tag {i}'}
    return _mock_keyword_data

@pytest.fixture
def create_keyword(mock_keyword_data):
    def _create_keyword(client, i=1):
        return Keyword(client=client, id=f'mock_id{i}', **mock_keyword_data(i))
    return _create_keyword

@pytest.fixture
def mock_publication_data():
    def _mock_publication_data(i=1, n_keywords=0):
        return {
            'author': f'mock author {i}',
            'published': bool(i%2),
            'title': f'mock publication {i}',
            'year': 1234+i,
            'journal': f'mock journal {i}',
            'journal_doi': f'mock journal doi {i}',
            'dataset_doi': f'mock dataset doi {i}',
            'description': f'mock description {i}',
            'public': bool(i%2),
            'download_link': f'mock download link {i}',
            'arxiv_id': f'mock arxiv id {i}',
            'keywords': [create_keyword(ik) for ik in range(n_keywords)]
        }
    return _mock_publication_data

@pytest.fixture
def create_publication(mock_publication_data):
    def _create_publication(client, i=1):
        return Publication(
            client=client,
            id=f'mock_id{i}',
            creation_time='2022-06-20T02:12:59.459297+00:00',
            **mock_publication_data(i))
    return _create_publication

@pytest.fixture
def mock_model_data():
    def _mock_model_data(i=1):
        return {
            'name': f'mock name {i}',
            'summary': f'mock summary {i}',
            'description': f'mock description {i}',
        }
    return _mock_model_data

@pytest.fixture
def create_model(mock_model_data):
    def _create_model(client, i=1):
        return Model(client=client, id=f'mock_id{i}', **mock_model_data(i))
    return _create_model

@pytest.fixture
def mock_dataset_data(create_publication, create_model):
    def _mock_dataset_data(client, i=1):
        return {
            'publication': create_publication(client, i),
            'model': create_model(client, i),
        }
    return _mock_dataset_data

@pytest.fixture
def create_dataset(mock_dataset_data):
    def _create_dataset(client, i=1):
        return Dataset(
            client=client,
            id=f'mock_id{i}',
            files=[f'mock_file{i}.h5'],
            **mock_dataset_data(client, i)
        )
    return _create_dataset

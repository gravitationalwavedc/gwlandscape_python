from pathlib import Path
from tempfile import NamedTemporaryFile

import pytest

from gwlandscape_python import GWLandscape
from gwlandscape_python.dataset_type import Dataset
from gwlandscape_python.keyword_type import Keyword
from gwlandscape_python.model_type import Model
from gwlandscape_python.publication_type import Publication
from gwlandscape_python.tests.utils import compare_graphql_query


@pytest.fixture
def setup_gwl_request(mocker):
    def mock_init(self, token, endpoint):
        pass

    mock_request = mocker.Mock()
    mocker.patch('gwlandscape_python.gwlandscape.GWDC.__init__', mock_init)
    mocker.patch('gwlandscape_python.gwlandscape.GWDC.request', mock_request)

    return GWLandscape(token='my_token'), mock_request


@pytest.fixture
def create_keyword_request(setup_gwl_request):
    response_data = [
        {
            "add_keyword": {
                "id": "S2V5d29yZE5vZGU6MzA="
            }
        },
        {
            "keywords": {
                "edges": [
                    {
                        "node": {
                            "id": "S2V5d29yZE5vZGU6MzA=",
                            "tag": "my_tag"
                        }
                    }
                ]
            }
        }
    ]

    gwl, mr = setup_gwl_request

    def mock_request(*args, **kwargs):
        return response_data.pop(0)

    mr.side_effect = mock_request

    return gwl, mr


@pytest.fixture
def create_publication_request(setup_gwl_request):
    response_data = [
        {
            "add_publication": {
                "id": "Q29tcGFzUHVibGljYXRpb25Ob2RlOjUw"
            }
        },
        {
            'compas_publications': {
                'edges': [
                    {
                        'node': {
                            'id': 'Q29tcGFzUHVibGljYXRpb25Ob2RlOjUw',
                            'author': 'my author',
                            'published': True,
                            'title': 'my publication',
                            'year': 1234,
                            'journal': 'journal',
                            'journal_doi': 'journal doi',
                            'dataset_doi': 'dataset doi',
                            'creation_time': '2022-06-20T02:12:59.459297+00:00',
                            'description': 'my description',
                            'public': True,
                            'download_link': 'my download link',
                            'arxiv_id': 'an arxiv id',
                            'keywords': {
                                'edges': [
                                    {
                                        'node': {
                                            'id': 'kw_id_1',
                                            'tag': 'keyword1'
                                        }
                                    },
                                    {
                                        'node': {
                                            'id': 'kw_id_2',
                                            'tag': 'keyword2'
                                        }
                                    }
                                ]
                            }
                        }
                    }
                ]
            }
        }
    ]

    gwl, mr = setup_gwl_request

    def mock_request(*args, **kwargs):
        return response_data.pop(0)

    mr.side_effect = mock_request

    return gwl, mr


@pytest.fixture
def create_model_request(setup_gwl_request):
    response_data = [
        {
            "add_compas_model": {
                "id": "Q29tcGFzTW9kZWxOb2RlOjI="
            }
        },
        {
            "compas_models": {
                "edges": [
                    {
                        "node": {
                            "id": "Q29tcGFzTW9kZWxOb2RlOjI=",
                            "name": "my_name",
                            "summary": "my_summary",
                            "description": "my_description"
                        }
                    }
                ]
            }
        }
    ]

    gwl, mr = setup_gwl_request

    def mock_request(*args, **kwargs):
        return response_data.pop(0)

    mr.side_effect = mock_request

    return gwl, mr


@pytest.fixture
def mock_publication_data():
    publication_data = {
        'id': 'Q29tcGFzUHVibGljYXRpb25Ob2RlOjUw',
        'author': 'my author',
        'published': True,
        'title': 'my publication',
        'year': 1234,
        'journal': 'journal',
        'journal_doi': 'journal doi',
        'dataset_doi': 'dataset doi',
        'creation_time': '2022-06-20T02:12:59.459297+00:00',
        'description': 'my description',
        'public': True,
        'download_link': 'my download link',
        'arxiv_id': 'an arxiv id',
        'keywords': []
    }

    model_data = {
        'name': 'my_name',
        'summary': 'my_summary',
        'description': 'my_description',
        'id': 'Q29tcGFzTW9kZWxOb2RlOjI='
    }

    return publication_data, model_data


@pytest.fixture
def create_dataset_request(setup_gwl_request, mock_publication_data):
    publication_data, model_data = mock_publication_data

    publication_data = publication_data.copy()
    publication_data['keywords'] = {
        'edges': []
    }

    response_data = [
        {
            "add_compas_dataset_model": {
                "id": "Q29tcGFzRGF0YXNldE1vZGVsTm9kZTo3="
            }
        },
        {
            "compas_dataset_models": {
                "edges": [
                    {
                        "node": {
                            "id": "Q29tcGFzRGF0YXNldE1vZGVsTm9kZTo3=",
                            "files": [
                                'test_file.h5'
                            ],
                            'compas_model': model_data,
                            'compas_publication': publication_data
                        }
                    }
                ]
            }
        }
    ]

    gwl, mr = setup_gwl_request

    def mock_request(*args, **kwargs):
        return response_data.pop(0)

    mr.side_effect = mock_request

    return gwl, mr


def test_create_keyword(create_keyword_request):
    gw, mock_request = create_keyword_request

    keyword = gw.create_keyword('my_tag')

    assert keyword.id == 'S2V5d29yZE5vZGU6MzA='
    assert keyword.tag == 'my_tag'

    assert compare_graphql_query(
        mock_request.mock_calls[0].args[0],
        """
            mutation AddKeywordMutation($input: AddKeywordMutationInput!) {
                addKeyword(input: $input) {
                    id
                }
            }
        """
    )

    assert mock_request.mock_calls[0].args[1] == {
        'input': {
            'tag': 'my_tag'
        }
    }

    assert compare_graphql_query(
        mock_request.mock_calls[1].args[0],
        """
            query {
                keywords (id: "S2V5d29yZE5vZGU6MzA=") {
                    edges {
                        node {
                            id
                            tag
                        }
                    }
                }
            }
        """
    )


def test_get_keyword_exact(setup_gwl_request):
    gwl, mock_request = setup_gwl_request

    mock_request.return_value = {
        "keywords": {
            "edges": [
                {
                    "node": {
                        "id": "S2V5d29yZE5vZGU6MzA=",
                        "tag": "my_tag"
                    }
                }
            ]
        }
    }

    kws = gwl.get_keywords(exact="my_tag")
    assert len(kws) == 1

    keyword = kws[0]
    assert keyword.id == 'S2V5d29yZE5vZGU6MzA='
    assert keyword.tag == 'my_tag'

    mock_request.assert_called_with(
        """
            query {
                keywords (tag: "my_tag") {
                    edges {
                        node {
                            id
                            tag
                        }
                    }
                }
            }
        """
    )


def test_get_keyword_contains(setup_gwl_request):
    gwl, mock_request = setup_gwl_request

    mock_request.return_value = {
        "keywords": {
            "edges": [
                {
                    "node": {
                        "id": "S2V5d29yZE5vZGU6MzA=",
                        "tag": "my_tag"
                    }
                }
            ]
        }
    }

    kws = gwl.get_keywords(contains="tag")
    assert len(kws) == 1

    keyword = kws[0]
    assert keyword.id == 'S2V5d29yZE5vZGU6MzA='
    assert keyword.tag == 'my_tag'

    mock_request.assert_called_with(
        """
            query {
                keywords (tag_Icontains: "tag") {
                    edges {
                        node {
                            id
                            tag
                        }
                    }
                }
            }
        """
    )


def test_get_keyword_id(setup_gwl_request):
    gwl, mock_request = setup_gwl_request

    mock_request.return_value = {
        "keywords": {
            "edges": [
                {
                    "node": {
                        "id": "S2V5d29yZE5vZGU6MzA=",
                        "tag": "my_tag"
                    }
                }
            ]
        }
    }

    kws = gwl.get_keywords(_id='S2V5d29yZE5vZGU6MzA=')
    assert len(kws) == 1

    keyword = kws[0]
    assert keyword.id == 'S2V5d29yZE5vZGU6MzA='
    assert keyword.tag == 'my_tag'

    mock_request.assert_called_with(
        """
            query {
                keywords (id: "S2V5d29yZE5vZGU6MzA=") {
                    edges {
                        node {
                            id
                            tag
                        }
                    }
                }
            }
        """
    )


def test_get_keyword_multi(setup_gwl_request):
    gwl, mock_request = setup_gwl_request

    mock_request.return_value = {
        "keywords": {
            "edges": [
                {
                    "node": {
                        "id": "S2V5d29yZE5vZGU6MzA=",
                        "tag": "my_tag"
                    }
                },
                {
                    "node": {
                        "id": "S2V5d29yZE5vZGU6MzB=",
                        "tag": "my_tag2"
                    }
                }
            ]
        }
    }

    kws = gwl.get_keywords()
    assert len(kws) == 2

    keyword = kws[0]
    assert keyword.id == 'S2V5d29yZE5vZGU6MzA='
    assert keyword.tag == 'my_tag'

    keyword = kws[1]
    assert keyword.id == 'S2V5d29yZE5vZGU6MzB='
    assert keyword.tag == 'my_tag2'

    mock_request.assert_called_with(
        """
            query {
                keywords  {
                    edges {
                        node {
                            id
                            tag
                        }
                    }
                }
            }
        """
    )


def test_delete_keyword(setup_gwl_request):
    gwl, mock_request = setup_gwl_request

    mock_request.return_value = {
        "delete_keyword": {
            "result": True
        }
    }

    keyword = Keyword(**{'tag': 'my_tag', 'id': 'S2V5d29yZE5vZGU6MzA='})

    gwl.delete_keyword(keyword)

    mock_request.assert_called_with(
        """
            mutation DeleteKeywordMutation($input: DeleteKeywordMutationInput!) {
                deleteKeyword(input: $input) {
                    result
                }
            }
        """,
        {
            'input': {
                'id': keyword.id
            }
        }
    )


def test_create_publication(create_publication_request):
    gw, mock_request = create_publication_request

    kws = [
        Keyword('kw_id_1', 'keyword1'),
        Keyword('kw_id_2', 'keyword2'),
    ]

    publication = gw.create_publication(
        'my author',
        'my publication',
        'an arxiv id',
        published=True,
        year=1234,
        journal="journal",
        journal_doi="journal doi",
        dataset_doi="dataset doi",
        description='my description',
        public=True,
        download_link='my download link',
        keywords=kws
    )

    assert publication.id == 'Q29tcGFzUHVibGljYXRpb25Ob2RlOjUw'
    assert publication.author == 'my author'
    assert publication.title == 'my publication'
    assert publication.arxiv_id == 'an arxiv id'
    assert publication.published is True
    assert publication.year == 1234
    assert publication.journal == "journal"
    assert publication.journal_doi == "journal doi"
    assert publication.dataset_doi == "dataset doi"
    assert publication.description == 'my description'
    assert publication.public is True
    assert publication.download_link == 'my download link'
    assert publication.keywords == kws

    assert compare_graphql_query(
        mock_request.mock_calls[0].args[0],
        """
            mutation AddPublicationMutation($input: AddPublicationMutationInput!) {
                addPublication(input: $input) {
                    id
                }
            }
        """
    )

    assert mock_request.mock_calls[0].args[1] == {
        'input': {
            'author': 'my author',
            'title': 'my publication',
            'arxiv_id': 'an arxiv id',
            'published': True,
            'year': 1234,
            'journal': "journal",
            'journal_doi': "journal doi",
            'dataset_doi': "dataset doi",
            'description': 'my description',
            'public': True,
            'download_link': 'my download link',
            'keywords': ['kw_id_1', 'kw_id_2']
        }
    }

    assert compare_graphql_query(
        mock_request.mock_calls[1].args[0],
        """
            query {
                compasPublications (id: "Q29tcGFzUHVibGljYXRpb25Ob2RlOjUw") {
                    edges {
                        node {
                            id
                            author
                            published
                            title
                            year
                            journal
                            journalDoi
                            datasetDoi
                            creationTime
                            description
                            public
                            downloadLink
                            arxivId
                            keywords {
                                edges {
                                    node {
                                        id
                                        tag
                                    }
                                }
                            }
                        }
                    }
                }
            }
        """
    )


def get_publication(gwl, mock_request, author=None, title=None, _id=None):
    mock_request.return_value = {
        'compas_publications': {
            'edges': [
                {
                    'node': {
                        'id': 'Q29tcGFzUHVibGljYXRpb25Ob2RlOjUw',
                        'author': 'my author',
                        'published': True,
                        'title': 'my publication',
                        'year': 1234,
                        'journal': 'journal',
                        'journal_doi': 'journal doi',
                        'dataset_doi': 'dataset doi',
                        'creation_time': '2022-06-20T02:12:59.459297+00:00',
                        'description': 'my description',
                        'public': True,
                        'download_link': 'my download link',
                        'arxiv_id': 'an arxiv id',
                        'keywords': {
                            'edges': [
                                {
                                    'node': {
                                        'id': 'kw_id_1',
                                        'tag': 'keyword1'
                                    }
                                },
                                {
                                    'node': {
                                        'id': 'kw_id_2',
                                        'tag': 'keyword2'
                                    }
                                }
                            ]
                        }
                    }
                }
            ]
        }
    }

    pub = gwl.get_publications(author, title, _id)
    assert len(pub) == 1

    publication = pub[0]

    kws = [
        Keyword('kw_id_1', 'keyword1'),
        Keyword('kw_id_2', 'keyword2'),
    ]

    assert publication.id == 'Q29tcGFzUHVibGljYXRpb25Ob2RlOjUw'
    assert publication.author == 'my author'
    assert publication.title == 'my publication'
    assert publication.arxiv_id == 'an arxiv id'
    assert publication.published is True
    assert publication.year == 1234
    assert publication.journal == "journal"
    assert publication.journal_doi == "journal doi"
    assert publication.dataset_doi == "dataset doi"
    assert publication.description == 'my description'
    assert publication.public is True
    assert publication.download_link == 'my download link'
    assert publication.keywords == kws


def test_get_publication_author(setup_gwl_request):
    gwl, mock_request = setup_gwl_request

    get_publication(gwl, mock_request, author='test_author')

    assert compare_graphql_query(
        mock_request.mock_calls[0].args[0],
        """
            query {
                compasPublications (author_Icontains: "test_author") {
                    edges {
                        node {
                            id
                            author
                            published
                            title
                            year
                            journal
                            journalDoi
                            datasetDoi
                            creationTime
                            description
                            public
                            downloadLink
                            arxivId
                            keywords {
                                edges {
                                    node {
                                        id
                                        tag
                                    }
                                }
                            }
                        }
                    }
                }
            }
        """
    )


def test_get_publication_title(setup_gwl_request):
    gwl, mock_request = setup_gwl_request

    get_publication(gwl, mock_request, title='test_title')

    assert compare_graphql_query(
        mock_request.mock_calls[0].args[0],
        """
            query {
                compasPublications (title_Icontains: "test_title") {
                    edges {
                        node {
                            id
                            author
                            published
                            title
                            year
                            journal
                            journalDoi
                            datasetDoi
                            creationTime
                            description
                            public
                            downloadLink
                            arxivId
                            keywords {
                                edges {
                                    node {
                                        id
                                        tag
                                    }
                                }
                            }
                        }
                    }
                }
            }
        """
    )


def test_get_publication_author_title(setup_gwl_request):
    gwl, mock_request = setup_gwl_request

    get_publication(gwl, mock_request, author='test_author', title='test_title')

    assert compare_graphql_query(
        mock_request.mock_calls[0].args[0],
        """
            query {
                compasPublications (title_Icontains: "test_title", author_Icontains: "test_author") {
                    edges {
                        node {
                            id
                            author
                            published
                            title
                            year
                            journal
                            journalDoi
                            datasetDoi
                            creationTime
                            description
                            public
                            downloadLink
                            arxivId
                            keywords {
                                edges {
                                    node {
                                        id
                                        tag
                                    }
                                }
                            }
                        }
                    }
                }
            }
        """
    )


def test_get_publication_author_title_id(setup_gwl_request):
    gwl, mock_request = setup_gwl_request

    with pytest.raises(AssertionError):
        get_publication(gwl, mock_request, author='test_author', title='test_title', _id='not_gonna_work')


def test_delete_publication(setup_gwl_request):
    gwl, mock_request = setup_gwl_request

    mock_request.return_value = {
        "delete_publication": {
            "result": True
        }
    }

    publication = Publication(**{
        'id': 'Q29tcGFzUHVibGljYXRpb25Ob2RlOjUw',
        'author': 'my author',
        'published': True,
        'title': 'my publication',
        'year': 1234,
        'journal': 'journal',
        'journal_doi': 'journal doi',
        'dataset_doi': 'dataset doi',
        'creation_time': '2022-06-20T02:12:59.459297+00:00',
        'description': 'my description',
        'public': True,
        'download_link': 'my download link',
        'arxiv_id': 'an arxiv id',
        'keywords': []
    })

    gwl.delete_publication(publication)

    mock_request.assert_called_with(
        """
            mutation DeletePublicationMutation($input: DeletePublicationMutationInput!) {
                deletePublication(input: $input) {
                    result
                }
            }
        """,
        {
            'input': {
                'id': publication.id
            }
        }
    )


def test_create_model(create_model_request):
    gw, mock_request = create_model_request

    model = gw.create_model('my_name', 'my_summary', 'my_description')

    assert model.id == 'Q29tcGFzTW9kZWxOb2RlOjI='
    assert model.name == 'my_name'
    assert model.summary == 'my_summary'
    assert model.description == 'my_description'

    assert compare_graphql_query(
        mock_request.mock_calls[0].args[0],
        """
            mutation AddCompasModelMutation($input: AddCompasModelMutationInput!) {
                addCompasModel(input: $input) {
                    id
                }
            }
        """
    )

    assert mock_request.mock_calls[0].args[1] == {
        'input': {
            'name': 'my_name',
            'summary': 'my_summary',
            'description': 'my_description'
        }
    }

    assert compare_graphql_query(
        mock_request.mock_calls[1].args[0],
        """
            query {
                compasModels (id: "Q29tcGFzTW9kZWxOb2RlOjI=") {
                    edges {
                        node {
                            id
                            name
                            summary
                            description
                        }
                    }
                }
            }
        """
    )


def get_model(gwl, mock_request, name=None, summary=None, description=None, _id=None):
    mock_request.return_value = {
        "compas_models": {
            "edges": [
                {
                    "node": {
                        "id": "Q29tcGFzTW9kZWxOb2RlOjI=",
                        "name": "my_name",
                        "summary": "my_summary",
                        "description": "my_description"
                    }
                }
            ]
        }
    }

    models = gwl.get_models(name, summary, description, _id)
    assert len(models) == 1

    model = models[0]

    assert model.id == 'Q29tcGFzTW9kZWxOb2RlOjI='
    assert model.name == 'my_name'
    assert model.summary == 'my_summary'
    assert model.description == 'my_description'


def test_get_models(setup_gwl_request):
    gwl, mock_request = setup_gwl_request

    get_model(gwl, mock_request)

    assert compare_graphql_query(
        mock_request.mock_calls[0].args[0],
        """
            query {
                compasModels {
                    edges {
                        node {
                            id
                            name
                            summary
                            description
                        }
                    }
                }
            }
        """
    )


def test_get_model_name_summary_description(setup_gwl_request):
    gwl, mock_request = setup_gwl_request

    get_model(gwl, mock_request, name='test_name', summary='test_summary', description='test_description')

    assert compare_graphql_query(
        mock_request.mock_calls[0].args[0],
        """
            query {
                compasModels (
                    name_Icontains: "test_name",
                    summary_Icontains: "test_summary",
                    description_Icontains: "test_description"
                ) {
                    edges {
                        node {
                            id
                            name
                            summary
                            description
                        }
                    }
                }
            }
        """
    )


def test_get_model_name_summary_description_id(setup_gwl_request):
    gwl, mock_request = setup_gwl_request

    with pytest.raises(AssertionError):
        get_model(
            gwl,
            mock_request,
            name='test_name',
            summary='test_summary',
            description='test_description',
            _id='not_gonna_work'
        )


def test_delete_model(setup_gwl_request):
    gwl, mock_request = setup_gwl_request

    mock_request.return_value = {
        "delete_compas_model": {
            "result": True
        }
    }

    model = Model(
        **{
            'name': 'my_name',
            'summary': 'my_summary',
            'description': 'my_description',
            'id': 'Q29tcGFzTW9kZWxOb2RlOjI='
        }
    )

    gwl.delete_model(model)

    mock_request.assert_called_with(
        """
            mutation DeleteCompasModelMutation($input: DeleteCompasModelMutationInput!) {
                deleteCompasModel(input: $input) {
                    result
                }
            }
        """,
        {
            'input': {
                'id': model.id
            }
        }
    )


def test_create_dataset(create_dataset_request, mock_publication_data):
    gw, mock_request = create_dataset_request
    publication_data, model_data = mock_publication_data

    publication = Publication(**publication_data)
    model = Model(**model_data)

    with NamedTemporaryFile() as tf:
        dataset = gw.create_dataset(publication, model, Path(tf.name))

    assert dataset.id == 'Q29tcGFzRGF0YXNldE1vZGVsTm9kZTo3='
    assert dataset.files == ['test_file.h5']

    for k, v in publication.__dict__.items():
        assert getattr(dataset.publication, k) == v

    for k, v in model.__dict__.items():
        assert getattr(dataset.model, k) == v

    assert compare_graphql_query(
        mock_request.mock_calls[0].args[0],
        """
            mutation AddCompasDatasetModelMutation($input: AddCompasDatasetModelMutationInput!) {
                addCompasDatasetModel(input: $input) {
                    id
                }
            }
        """
    )

    assert mock_request.mock_calls[0].args[1]['input']['compas_publication'] == publication.id
    assert mock_request.mock_calls[0].args[1]['input']['compas_model'] == model.id
    assert 'file' in mock_request.mock_calls[0].args[1]['input']

    assert compare_graphql_query(
        mock_request.mock_calls[1].args[0],
        """
            query {
                compasDatasetModels (id: "Q29tcGFzRGF0YXNldE1vZGVsTm9kZTo3=") {
                    edges {
                        node {
                            id
                            files
                            compasPublication {
                                id
                                author
                                published
                                title
                                year
                                journal
                                journalDoi
                                datasetDoi
                                creationTime
                                description
                                public
                                downloadLink
                                arxivId
                                keywords {
                                    edges {
                                        node {
                                            id
                                            tag
                                        }
                                    }
                                }
                            }
                            compasModel {
                                id
                                name
                                summary
                                description
                            }
                        }
                    }
                }
            }
        """
    )


def get_dataset(gwl, mock_request, mock_publication_data, publication=None, model=None, _id=None):
    publication_data, model_data = mock_publication_data

    publication_data = publication_data.copy()
    publication_data['keywords'] = {
        'edges': []
    }

    mock_request.return_value = {
        "compas_dataset_models": {
            "edges": [
                {
                    "node": {
                        "id": "Q29tcGFzRGF0YXNldE1vZGVsTm9kZTo3=",
                        "files": [
                            'test_file.h5'
                        ],
                        'compas_model': model_data,
                        'compas_publication': publication_data
                    }
                }
            ]
        }
    }

    datasets = gwl.get_datasets(publication, model, _id)
    assert len(datasets) == 1


def test_get_datasets(setup_gwl_request, mock_publication_data):
    gwl, mock_request = setup_gwl_request

    get_dataset(gwl, mock_request, mock_publication_data)

    assert compare_graphql_query(
        mock_request.mock_calls[0].args[0],
        """
            query {
                compasDatasetModels {
                    edges {
                        node {
                            id
                            files
                            compasPublication {
                                id
                                author
                                published
                                title
                                year
                                journal
                                journalDoi
                                datasetDoi
                                creationTime
                                description
                                public
                                downloadLink
                                arxivId
                                keywords {
                                    edges {
                                        node {
                                            id
                                            tag
                                        }
                                    }
                                }
                            }
                            compasModel {
                                id
                                name
                                summary
                                description
                            }
                        }
                    }
                }
            }
        """
    )


def test_get_dataset_publication_model(setup_gwl_request, mock_publication_data):
    gwl, mock_request = setup_gwl_request
    publication_data, model_data = mock_publication_data

    publication = Publication(**publication_data)
    model = Model(**model_data)

    get_dataset(gwl, mock_request, mock_publication_data, publication, model)

    assert compare_graphql_query(
        mock_request.mock_calls[0].args[0],
        """
            query {
                compasDatasetModels (
                    compasPublication: "Q29tcGFzUHVibGljYXRpb25Ob2RlOjUw",
                    compasModel: "Q29tcGFzTW9kZWxOb2RlOjI="
                ) {
                    edges {
                        node {
                            id
                            files
                            compasPublication {
                                id
                                author
                                published
                                title
                                year
                                journal
                                journalDoi
                                datasetDoi
                                creationTime
                                description
                                public
                                downloadLink
                                arxivId
                                keywords {
                                    edges {
                                        node {
                                            id
                                            tag
                                        }
                                    }
                                }
                            }
                            compasModel {
                                id
                                name
                                summary
                                description
                            }
                        }
                    }
                }
            }
        """
    )


def test_get_dataset_publication_model_id(setup_gwl_request, mock_publication_data):
    gwl, mock_request = setup_gwl_request
    publication_data, model_data = mock_publication_data

    publication = Publication(**publication_data)
    model = Model(**model_data)

    with pytest.raises(AssertionError):
        get_dataset(
            gwl,
            mock_request,
            mock_publication_data,
            publication,
            model,
            'not_gonna_work'
        )


def test_delete_dataset(setup_gwl_request, mock_publication_data):
    gwl, mock_request = setup_gwl_request
    publication_data, model_data = mock_publication_data

    mock_request.return_value = {
        "delete_compas_dataset_model": {
            "result": True
        }
    }

    publication = Publication(**publication_data)
    model = Model(**model_data)

    dataset = Dataset(**{
        'id': 'Q29tcGFzRGF0YXNldE1vZGVsTm9kZTo3=',
        'publication': publication,
        'model': model,
        'files': ['my_file.h5']
    })

    gwl.delete_dataset(dataset)

    mock_request.assert_called_with(
        """
            mutation DeleteCompasDatasetModelMutation($input: DeleteCompasDatasetModelMutationInput!) {
                deleteCompasDatasetModel(input: $input) {
                    result
                }
            }
        """,
        {
            'input': {
                'id': dataset.id
            }
        }
    )

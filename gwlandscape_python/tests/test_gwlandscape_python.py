import uuid
from pathlib import Path
from tempfile import NamedTemporaryFile

import pytest

from gwlandscape_python.keyword_type import Keyword
from gwlandscape_python.model_type import Model
from gwlandscape_python.publication_type import Publication
from gwlandscape_python.tests.utils import compare_graphql_query


@pytest.fixture
def create_keyword_request(setup_gwl_request, query_keyword_return):
    response_data = [
        {
            "add_keyword": {
                "id": "mock_keyword_id1"
            }
        },
        query_keyword_return(n_keywords=1)
    ]

    gwl, mr = setup_gwl_request

    def mock_request(*args, **kwargs):
        return response_data.pop(0)

    mr.side_effect = mock_request

    return gwl, mr


@pytest.fixture
def get_keywords_query():
    return """
        query ($exact: String, $contains: String, $id: ID) {
            keywords (tag: $exact, tag_Icontains: $contains, id: $id) {
                edges {
                    node {
                        id
                        tag
                    }
                }
            }
        }
    """


@pytest.fixture
def create_publication_request(setup_gwl_request, query_publication_return):
    response_data = [
        {
            "add_publication": {
                "id": "mock_publication_id1"
            }
        },
        query_publication_return(n_publications=1)
    ]

    gwl, mr = setup_gwl_request

    def mock_request(*args, **kwargs):
        return response_data.pop(0)

    mr.side_effect = mock_request

    return gwl, mr


@pytest.fixture
def get_publications_query():
    return """
        query ($author: String, $title: String, $id: ID) {
            compasPublications (
                author_Icontains: $author,
                title_Icontains: $title,
                id: $id
            ) {
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


@pytest.fixture
def create_model_request(setup_gwl_request, query_model_return):
    response_data = [
        {
            "add_compas_model": {
                "id": "mock_model_id1"
            }
        },
        query_model_return(n_models=1)
    ]

    gwl, mr = setup_gwl_request

    def mock_request(*args, **kwargs):
        return response_data.pop(0)

    mr.side_effect = mock_request

    return gwl, mr


@pytest.fixture
def get_models_query():
    return """
        query ($name: String, $summary: String, $description: String, $id: ID) {
            compasModels (
                name_Icontains: $name,
                summary_Icontains: $summary,
                description_Icontains: $description,
                id: $id
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


@pytest.fixture
def create_dataset_request(setup_gwl_request, query_dataset_return):
    print(query_dataset_return(n_datasets=1))
    response_data = [
        {
            "generate_compas_dataset_model_upload_token": {
                "token": str(uuid.uuid4())
            }
        },
        {
            "upload_compas_dataset_model": {
                "id": "mock_dataset_id1"
            }
        },
        query_dataset_return(n_datasets=1)
    ]

    gwl, mr = setup_gwl_request

    def mock_request(*args, **kwargs):
        return response_data.pop(0)

    mr.side_effect = mock_request

    return gwl, mr


@pytest.fixture
def get_datasets_query():
    return """
        query ($publication: ID, $model: ID, $id: ID) {
            compasDatasetModels (compasPublication: $publication, compasModel: $model, id: $id) {
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


def test_create_keyword(create_keyword_request, mock_keyword_data, get_keywords_query):
    gwl, mock_request = create_keyword_request

    keyword_data = mock_keyword_data(i=1)
    keyword_id = 'mock_keyword_id1'

    keyword = gwl.create_keyword(**keyword_data)
    
    assert keyword.id == keyword_id
    assert keyword.tag == keyword_data['tag']

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

    assert mock_request.mock_calls[0].args[1] == {'input': keyword_data}

    assert compare_graphql_query(
        mock_request.mock_calls[1].kwargs['query'],
        get_keywords_query
    )

    assert mock_request.mock_calls[1].kwargs['variables'] == {
        'exact': None,
        'contains': None,
        'id': keyword_id
    }


def test_get_keyword_exact(setup_gwl_request, query_keyword_return, mock_keyword_data, get_keywords_query):
    gwl, mock_request = setup_gwl_request

    keyword_data = mock_keyword_data(i=1)
    keyword_id = 'mock_keyword_id1'

    mock_request.return_value = query_keyword_return(n_keywords=1)

    kws = gwl.get_keywords(exact=keyword_data['tag'])
    assert len(kws) == 1

    keyword = kws[0]
    assert keyword.id == keyword_id
    assert keyword.tag == keyword_data['tag']

    assert compare_graphql_query(
        mock_request.mock_calls[0].kwargs['query'],
        get_keywords_query
    )

    assert mock_request.mock_calls[0].kwargs['variables'] == {
        'exact': keyword_data['tag'],
        'contains': None,
        'id': None
    }


def test_get_keyword_contains(setup_gwl_request, query_keyword_return, mock_keyword_data, get_keywords_query):
    gwl, mock_request = setup_gwl_request

    keyword_data = mock_keyword_data(i=1)
    keyword_id = 'mock_keyword_id1'

    mock_request.return_value = query_keyword_return(n_keywords=1)

    kws = gwl.get_keywords(contains=keyword_data['tag'])
    assert len(kws) == 1

    keyword = kws[0]
    assert keyword.id == keyword_id
    assert keyword.tag == keyword_data['tag']

    assert compare_graphql_query(
        mock_request.mock_calls[0].kwargs['query'],
        get_keywords_query
    )

    assert mock_request.mock_calls[0].kwargs['variables'] == {
        'exact': None,
        'contains': keyword_data['tag'],
        'id': None
    }


def test_get_keyword_id(setup_gwl_request, query_keyword_return, mock_keyword_data, get_keywords_query):
    gwl, mock_request = setup_gwl_request

    keyword_data = mock_keyword_data(i=1)
    keyword_id = 'mock_keyword_id1'

    mock_request.return_value = query_keyword_return(n_keywords=1)

    kws = gwl.get_keywords(_id=keyword_id)
    assert len(kws) == 1

    keyword = kws[0]
    assert keyword.id == keyword_id
    assert keyword.tag == keyword_data['tag']

    assert compare_graphql_query(
        mock_request.mock_calls[0].kwargs['query'],
        get_keywords_query
    )

    assert mock_request.mock_calls[0].kwargs['variables'] == {
        'exact': None,
        'contains': None,
        'id': keyword_id
    }


def test_get_keyword_multi(setup_gwl_request, query_keyword_return, mock_keyword_data, get_keywords_query):
    gwl, mock_request = setup_gwl_request

    keywords_data = [mock_keyword_data(i+1) for i in range(2)]

    mock_request.return_value = query_keyword_return(n_keywords=2)

    kws = gwl.get_keywords()
    assert len(kws) == 2

    for i, keyword_data in enumerate(keywords_data):
        assert kws[i].id == f'mock_keyword_id{i+1}'
        assert kws[i].tag == keyword_data['tag']

    assert compare_graphql_query(
        mock_request.mock_calls[0].kwargs['query'],
        get_keywords_query
    )

    assert mock_request.mock_calls[0].kwargs['variables'] == {
        'exact': None,
        'contains': None,
        'id': None
    }


def test_create_publication(create_publication_request, mock_publication_data, get_publications_query):
    gwl, mock_request = create_publication_request

    publication_data = mock_publication_data(i=1, n_keywords=2)
    publication_id = 'mock_publication_id1'

    publication = gwl.create_publication(**publication_data)

    assert publication.id == publication_id
    for key, val in publication_data.items():
        assert getattr(publication, key) == val

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

    publication_data['keywords'] = [keyword.id for keyword in publication_data['keywords']]
    assert mock_request.mock_calls[0].args[1] == {'input': publication_data}

    assert compare_graphql_query(
        mock_request.mock_calls[1].kwargs['query'],
        get_publications_query
    )

    assert mock_request.mock_calls[1].kwargs['variables'] == {
        'author': None,
        'title': None,
        'id': publication_id
    }



def test_get_publication_author(
    setup_gwl_request,
    query_publication_return,
    mock_publication_data,
    get_publications_query
):
    gwl, mock_request = setup_gwl_request

    publication_data = mock_publication_data(1, n_keywords=2)
    publication_id = 'mock_publication_id1'

    mock_request.return_value = query_publication_return(n_publications=1)

    publications = gwl.get_publications(author=publication_data['author'])
    assert len(publications) == 1

    publication = publications[0]

    assert publication.id == publication_id
    for key, val in publication_data.items():
        assert getattr(publication, key) == val

    assert compare_graphql_query(
        mock_request.mock_calls[0].kwargs['query'],
        get_publications_query
    )

    assert mock_request.mock_calls[0].kwargs['variables'] == {
        'author': publication_data['author'],
        'title': None,
        'id': None
    }


def test_get_publication_title(
    setup_gwl_request,
    query_publication_return,
    mock_publication_data,
    get_publications_query
):
    gwl, mock_request = setup_gwl_request

    publication_data = mock_publication_data(1, n_keywords=2)
    publication_id = 'mock_publication_id1'

    mock_request.return_value = query_publication_return(n_publications=1)

    publications = gwl.get_publications(title=publication_data['title'])
    assert len(publications) == 1

    publication = publications[0]

    assert publication.id == publication_id
    for key, val in publication_data.items():
        assert getattr(publication, key) == val

    assert compare_graphql_query(
        mock_request.mock_calls[0].kwargs['query'],
        get_publications_query
    )

    assert mock_request.mock_calls[0].kwargs['variables'] == {
        'author': None,
        'title': publication_data['title'],
        'id': None
    }


def test_get_publication_author_title(
    setup_gwl_request,
    query_publication_return,
    mock_publication_data,
    get_publications_query
):
    gwl, mock_request = setup_gwl_request

    publication_data = mock_publication_data(1, n_keywords=2)
    publication_id = 'mock_publication_id1'

    mock_request.return_value = query_publication_return(n_publications=1)

    publications = gwl.get_publications(title=publication_data['title'], author=publication_data['author'])
    assert len(publications) == 1

    publication = publications[0]

    assert publication.id == publication_id
    for key, val in publication_data.items():
        assert getattr(publication, key) == val

    assert compare_graphql_query(
        mock_request.mock_calls[0].kwargs['query'],
        get_publications_query
    )

    assert mock_request.mock_calls[0].kwargs['variables'] == {
        'author': publication_data['author'],
        'title': publication_data['title'],
        'id': None
    }


def test_get_publication_author_title_id(setup_gwl_request):
    gwl, mock_request = setup_gwl_request

    with pytest.raises(SyntaxError):
        gwl.get_publications(author='all', title='together', _id='not_gonna_work')


def test_create_model(create_model_request, mock_model_data, get_models_query):
    gwl, mock_request = create_model_request

    model_data = mock_model_data(i=1)
    model_id = 'mock_model_id1'

    model = gwl.create_model(**model_data)

    assert model.id == model_id
    for key, val in model_data.items():
        assert getattr(model, key) == val

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

    assert mock_request.mock_calls[0].args[1] == {'input': model_data}

    assert compare_graphql_query(
        mock_request.mock_calls[1].kwargs['query'],
        get_models_query
    )

    assert mock_request.mock_calls[1].kwargs['variables'] == {
        'name': None,
        'summary': None,
        'description': None,
        'id': model_id
    }


def test_get_models(setup_gwl_request, query_model_return, mock_model_data, get_models_query):
    gwl, mock_request = setup_gwl_request

    model_data = mock_model_data(i=1)
    model_id = 'mock_model_id1'

    mock_request.return_value = query_model_return(1)

    models = gwl.get_models()
    assert len(models) == 1

    model = models[0]

    assert model.id == model_id
    for key, val in model_data.items():
        assert getattr(model, key) == val

    assert compare_graphql_query(
        mock_request.mock_calls[0].kwargs['query'],
        get_models_query
    )

    assert mock_request.mock_calls[0].kwargs['variables'] == {
        'name': None,
        'summary': None,
        'description': None,
        'id': None
    }


def test_get_models_name_summary_description(
    setup_gwl_request,
    query_model_return,
    mock_model_data,
    get_models_query
):
    gwl, mock_request = setup_gwl_request

    model_data = mock_model_data(i=1)
    model_id = 'mock_model_id1'

    mock_request.return_value = query_model_return(1)

    models = gwl.get_models(
        name=model_data['name'],
        summary=model_data['summary'],
        description=model_data['description'],
    )
    assert len(models) == 1

    model = models[0]

    assert model.id == model_id
    for key, val in model_data.items():
        assert getattr(model, key) == val

    assert compare_graphql_query(
        mock_request.mock_calls[0].kwargs['query'],
        get_models_query
    )

    assert mock_request.mock_calls[0].kwargs['variables'] == {
            'name': model_data['name'],
            'summary': model_data['summary'],
            'description': model_data['description'],
            'id': None
        }


def test_get_model_name_summary_description_id(setup_gwl_request):
    gwl, mock_request = setup_gwl_request

    with pytest.raises(SyntaxError):
        gwl.get_models(name='this', summary='will', description='not', _id='work')


def test_create_dataset(create_dataset_request, mock_dataset_data, get_datasets_query):
    gwl, mock_request = create_dataset_request

    dataset_data = mock_dataset_data(gwl, i=1)
    dataset_id = 'mock_dataset_id1'

    with NamedTemporaryFile() as tf:
        dataset = gwl.create_dataset(dataset_data['publication'], dataset_data['model'], Path(tf.name))

    assert dataset.id == dataset_id
    assert dataset.files == ['mock_file1.h5']

    publication, model = dataset.publication, dataset.model

    for key, val in publication.__dict__.items():
        assert getattr(dataset.publication, key) == val

    for key, val in model.__dict__.items():
        assert getattr(dataset.model, key) == val

    assert compare_graphql_query(
        mock_request.mock_calls[0].kwargs['query'],
        """
            query GenerateCompasDatasetModelUploadToken {
                generateCompasDatasetModelUploadToken {
                  token
                }
            }
        """
    )

    assert compare_graphql_query(
        mock_request.mock_calls[1].kwargs['query'],
        """
            mutation UploadCompasDatasetModelMutation($input: UploadCompasDatasetModelMutationInput!) {
                uploadCompasDatasetModel(input: $input) {
                    id
                }
            }
        """
    )

    assert mock_request.mock_calls[1].kwargs['variables']['input']['compas_publication'] == publication.id
    assert mock_request.mock_calls[1].kwargs['variables']['input']['compas_model'] == model.id
    assert 'jobFile' in mock_request.mock_calls[1].kwargs['variables']['input']

    assert compare_graphql_query(
        mock_request.mock_calls[2].kwargs['query'],
        get_datasets_query
    )

    assert mock_request.mock_calls[2].kwargs['variables'] == {
        'publication': None,
        'model': None,
        'id': dataset_id
    }


def test_get_datasets(setup_gwl_request, query_dataset_return, mock_dataset_data, get_datasets_query):
    gwl, mock_request = setup_gwl_request

    dataset_data = mock_dataset_data(gwl, i=1)
    dataset_id = 'mock_dataset_id1'

    mock_request.return_value = query_dataset_return(1)

    datasets = gwl.get_datasets()
    assert len(datasets) == 1

    dataset = datasets[0]

    assert dataset.id == dataset_id
    for key, val in dataset_data.items():
        assert getattr(dataset, key) == val

    assert compare_graphql_query(
        mock_request.mock_calls[0].kwargs['query'],
        get_datasets_query
    )

    assert mock_request.mock_calls[0].kwargs['variables'] == {
        'publication': None,
        'model': None,
        'id': None
    }


def test_get_datasets_publication_model(
    setup_gwl_request,
    query_dataset_return,
    mock_dataset_data,
    get_datasets_query
):
    gwl, mock_request = setup_gwl_request

    dataset_data = mock_dataset_data(gwl, i=1)
    dataset_id = 'mock_dataset_id1'

    mock_request.return_value = query_dataset_return(1)

    datasets = gwl.get_datasets(**dataset_data)
    assert len(datasets) == 1

    dataset = datasets[0]

    assert dataset.id == dataset_id
    for key, val in dataset_data.items():
        assert getattr(dataset, key) == val

    assert compare_graphql_query(
        mock_request.mock_calls[0].kwargs['query'],
        get_datasets_query
    )

    assert mock_request.mock_calls[0].kwargs['variables'] == {
        'id': None,
        'publication': 'mock_publication_id1',
        'model': 'mock_model_id1'
    }


def test_get_datasets_publication_model_id(
    setup_gwl_request,
    mock_dataset_data,
):
    gwl, mock_request = setup_gwl_request

    with pytest.raises(SyntaxError):
        gwl.get_datasets(_id='not_gonna_work', **mock_dataset_data(gwl, i=1))

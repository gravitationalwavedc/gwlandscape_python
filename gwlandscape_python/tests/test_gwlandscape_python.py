import pytest

from gwlandscape_python import GWLandscape
from gwlandscape_python.keyword_type import Keyword


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


def test_create_keyword(create_keyword_request):
    gw, mock_request = create_keyword_request

    keyword = gw.create_keyword('my_tag')

    assert keyword.id == 'S2V5d29yZE5vZGU6MzA='
    assert keyword.tag == 'my_tag'

    mock_request.mock_calls[0].assert_called_with(
        """
            mutation AddKeywordMutation($input: AddKeywordMutationInput!) {
                addKeyword(input: $input) {
                    id
                }
            }
        """,
        {
            'input': {
                'tag': "my_tag"
            }
        }
    )

    mock_request.mock_calls[1].assert_called_with(
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

    keyword = Keyword({'tag': 'my_tag', 'id': 'S2V5d29yZE5vZGU6MzA='})

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

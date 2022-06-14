import pytest

from gwlandscape_python import GWLandscape


@pytest.fixture
def mock_gwdc_init(mocker):
    def mock_init(self, token, endpoint):
        pass

    mocker.patch('gwdc_python.gwdc.GWDC.__init__', mock_init)


@pytest.fixture
def setup_mock_gwdc(mocker, mock_gwdc_init):
    def mock_gwdc(request_data):
        mock_request = mocker.Mock(return_value=request_data)
        mocker.patch('gwdc_python.gwdc.GWDC.request', mock_request)

    return mock_gwdc


@pytest.fixture
def setup_mock_gwdc_multi(mocker, mock_gwdc_init):
    def mock_gwdc(request_data):
        def mock_request(*args, **kwargs):
            return request_data.pop(0)

        mocker.patch('gwdc_python.gwdc.GWDC.request', mock_request)

    return mock_gwdc


@pytest.fixture
def create_keyword_request(setup_mock_gwdc_multi):
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
    setup_mock_gwdc_multi(response_data)

    return response_data


def test_constructor(mock_gwdc_init):
    gw = GWLandscape(token='test_token')
    assert gw.request == gw.client.request


def test_create_keyword(create_keyword_request):
    gw = GWLandscape(token='my_token')

    keyword = gw.create_keyword('my_tag')

    assert keyword.id == 'S2V5d29yZE5vZGU6MzA='
    assert keyword.tag == 'my_tag'
    

# def test_get_keyword_exact(get_keyword_request):
#     gw = GWLandscape(token='my_token')
#
#     keyword = gw.get_keywords('my_tag')
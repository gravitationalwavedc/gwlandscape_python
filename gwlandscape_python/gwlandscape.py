from gwdc_python import GWDC
from gwdc_python.logger import create_logger

from .keyword_type import Keyword
from .settings import GWLANDSCAPE_ENDPOINT

logger = create_logger(__name__)


class GWLandscape:
    """
    GWLandscape class provides an API for interacting with COMPAS, allowing jobs to be submitted and acquired.

    Parameters
    ----------
    token : str
        API token for a GWDC user
    endpoint : str, optional
        URL to which we send the queries, by default GWLANDSCAPE_ENDPOINT

    Attributes
    ----------
    client : GWDC
        Handles a lot of the underlying logic surrounding the queries
    """

    def __init__(self, token, endpoint=GWLANDSCAPE_ENDPOINT):
        self.client = GWDC(token=token, endpoint=endpoint)
        self.request = self.client.request  # Setting shorthand for simplicity

    def create_keyword(self, tag):
        """
        Creates a new keyword object with the specified tag.

        Parameters
        ----------
        tag : str
            The tag of the keyword to be created

        Return
        ------
        Keyword instance representing the keyword created
        """
        mutation = """
            mutation AddKeywordMutation($input: AddKeywordMutationInput!) {
                addKeyword(input: $input) {
                    id
                }
            }
        """

        params = {
            'input': {
                'tag': tag
            }
        }

        result = self.request(mutation, params)

        assert 'id' in result['add_keyword']

        return self.get_keywords(_id=result['add_keyword']['id'])[0]

    def get_keywords(self, exact=None, contains=None, _id=None):
        """
        Fetch all keywords matching exactly the provided parameter, any keywords with tags containing the term in
        the contains parameter, or the keyword with the specified id.

        At most, only one of exact, contains, or _id must be provided. If neither the extract, contains, or _id
        parameter is supplied, then all keywords are returned.

        Parameters
        ----------
        exact : str, optional
            Match keywords with this exact tag (case-insensitive)
        contains : str, optional
            Match keywords containing this text (case-insensitive))
        _id : str, optional
            Match keyword by the provided ID

        Return
        ------
        A list of Keyword instances. If nothing was found the list will be empty.
        """

        # Make sure exactly one parameter is provided
        assert sum(x is not None for x in (exact, contains, _id)) <= 1

        keyword_component = ''
        if exact:
            keyword_component = f'(tag: "{exact}")'

        if contains:
            keyword_component = f'(tag_Icontains: "{contains}")'

        if _id:
            keyword_component = f'(id: "{_id}")'

        query = f"""
            query {{
                keywords {keyword_component} {{
                    edges {{
                        node {{
                            id
                            tag
                        }}
                    }}
                }}
            }}
        """

        result = self.request(query)

        return [Keyword(kw['node']) for kw in result['keywords']['edges']]

    def delete_keyword(self, keyword):
        """
        Delete a keyword represented by the provided keyword.

        Parameters
        ----------
        keyword: Keyword
            The Keyword instance to delete

        Return
        ------
        None
        """

        mutation = """
            mutation DeleteKeywordMutation($input: DeleteKeywordMutationInput!) {
                deleteKeyword(input: $input) {
                    result
                }
            }
        """

        params = {
            'input': {
                'id': keyword.id
            }
        }

        result = self.request(mutation, params)

        assert result['delete_keyword']['result']

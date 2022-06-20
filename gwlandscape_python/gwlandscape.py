from gwdc_python import GWDC
from gwdc_python.logger import create_logger

from .keyword_type import Keyword
from .publication_type import Publication
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

        return [Keyword(**kw['node']) for kw in result['keywords']['edges']]

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

    def create_publication(self, author, title, arxiv_id, **kwargs):
        """
        Creates a new keyword object with the specified tag.

        Parameters
        ----------
        author : str
            The author of the publication
        title : str
            The title of the publication
        arxiv_id : str
            The arxiv id of the publication
        **kwargs
            Possible kwargs for a publication:
            published : bool
                If the publication was published in a journal/arxiv
            year : int
                The year of the publication
            journal : str
                The name of the journal
            journal_doi : str
                The DOI of the publication
            dataset_doi : str
                The DOI of the dataset
            description : str
                A description of the publication
            public : bool
                If the publication has been made public (visible to the public)
            download_link : str
                A link to download the publication/dataset
            keywords : list [Keyword]
                A list of keywords for the publication

        Return
        ------
        Publication instance representing the publication created
        """
        mutation = """
            mutation AddPublicationMutation($input: AddPublicationMutationInput!) {
                addPublication(input: $input) {
                    id
                }
            }
        """

        params = {
            'input': {
                'author': author,
                'title': title,
                'arxiv_id': arxiv_id,
                **kwargs
            }
        }

        # Handle keywords
        if 'keywords' in params['input']:
            params['input']['keywords'] = [k.id for k in params['input']['keywords']]

        result = self.request(mutation, params)

        assert 'id' in result['add_publication']

        return self.get_publications(_id=result['add_publication']['id'])[0]

    def get_publications(self, author=None, title=None, _id=None):
        """
        Fetch all publications with author/title/arxiv id containing the values specified.
        Also allows fetching publication by the provided ID

        At most, only one of (author, title) or _id must be provided. If no parameter is provided, all
        publications are returned.

        Parameters
        ----------
        author : str, optional
            Match publication author contains this value (case-insensitive)
        title : str, optional
            Match publication arxiv id exactly equals this value (case-insensitive)
        _id : str, optional
            Match publication by the provided ID

        Return
        ------
        A list of Publication instances. If nothing was found the list will be empty.
        """

        # Make sure exactly one parameter is provided
        param_provided = author or title
        if param_provided:
            assert not _id

        if _id:
            assert not param_provided

        keyword_component = []
        if title:
            keyword_component.append(f'title_Icontains: "{title}"')

        if author:
            keyword_component.append(f'author_Icontains: "{author}"')

        if _id:
            keyword_component.append(f'id: "{_id}"')

        query = f"""
            query {{
                compasPublications {'' if not keyword_component else ('(' + ','.join(keyword_component) + ')')} {{
                    edges {{
                        node {{
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
                            keywords {{
                                edges {{
                                    node {{
                                        id
                                        tag
                                    }}
                                }}
                            }}
                        }}
                    }}
                }}
            }}
        """

        result = self.request(query)

        # Handle keywords
        for pub in result['compas_publications']['edges']:
            pub['node']['keywords'] = [Keyword(**kw['node']) for kw in pub['node']['keywords']['edges']]

        return [Publication(**kw['node']) for kw in result['compas_publications']['edges']]

    def delete_publication(self, publication):
        """
        Delete a publication represented by the provided publication instance.

        Parameters
        ----------
        publication: Publication
            The Publication instance to delete

        Return
        ------
        None
        """

        mutation = """
            mutation DeletePublicationMutation($input: DeletePublicationMutationInput!) {
                deletePublication(input: $input) {
                    result
                }
            }
        """

        params = {
            'input': {
                'id': publication.id
            }
        }

        result = self.request(mutation, params)

        assert result['delete_publication']['result']

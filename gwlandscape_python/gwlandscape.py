from pathlib import Path

from gwdc_python import GWDC
from gwdc_python.logger import create_logger

from .dataset_type import Dataset
from .keyword_type import Keyword
from .model_type import Model
from .publication_type import Publication
from .utils import mutually_exclusive
from .settings import GWLANDSCAPE_ENDPOINT, GWLANDSCAPE_AUTH_ENDPOINT

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

    def __init__(self, token="", auth_endpoint=GWLANDSCAPE_AUTH_ENDPOINT, endpoint=GWLANDSCAPE_ENDPOINT):
        self.client = GWDC(
            token=token,
            auth_endpoint=auth_endpoint,
            endpoint=endpoint,
        )

        self.request = self.client.request  # Setting shorthand for simplicity

    def create_keyword(self, tag):
        """
        Creates a new keyword object with the specified tag.

        Parameters
        ----------
        tag : str
            The tag of the keyword to be created

        Returns
        -------
        Keyword
            Created Keyword
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

    @mutually_exclusive('exact', 'contains', '_id')
    def get_keywords(self, exact=None, contains=None, _id=None):
        """
        Fetch all keywords matching exactly the provided parameter, any keywords with tags containing the term in
        the contains parameter, or the keyword with the specified id.

        At most, only one of exact, contains, or _id must be provided. If neither the extract, contains, or _id
        parameter is supplied, then all keywords are returned.

        Parameters
        ----------
        exact : str, optional
            Match keywords with this exact tag (case-insensitive), by default None
        contains : str, optional
            Match keywords containing this text (case-insensitive)), by default None
        _id : str, optional
            Match keyword by the provided ID, by default None

        Returns
        -------
        list
            A list of :class:`.Keyword` instances
        """

        query = """
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

        variables = {
            'exact': exact,
            'contains': contains,
            'id': _id
        }

        result = self.request(query=query, variables=variables)

        return [Keyword(**kw['node']) for kw in result['keywords']['edges']]

    def delete_keyword(self, keyword):
        """
        Delete a keyword represented by the provided keyword.

        Parameters
        ----------
        keyword: Keyword
            The Keyword instance to delete
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
        **kwargs : dict, optional
            Extra keyword arguments that are provided to GWLandscape to create a publication.
            Accepted keys are:

            published: (`bool`)
                If the publication was published in a journal/arXiv
            year : (`int`)
                The year of the publication
            journal : (`str`)
                The name of the journal
            journal_doi : (`str`)
                The DOI of the publication
            dataset_doi : (`str`)
                The DOI of the dataset
            description : (`str`)
                A description of the publication
            public : (`bool`)
                If the publication has been made public (visible to the public)
            download_link : (`str`)
                A link to download the publication/dataset
            keywords : (`list`)
                A list of :class:`~.Keyword` objects for the publication

        Returns
        -------
        Publication
            Created Publication
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

    @mutually_exclusive('author | title', '_id')
    def get_publications(self, author=None, title=None, _id=None):
        """
        Fetch all publications with author/title/arxiv id containing the values specified.
        Also allows fetching publication by the provided ID

        At most, only one of (author, title) or _id must be provided. If no parameter is provided, all
        publications are returned.

        Parameters
        ----------
        author : str, optional
            Match publication author contains this value (case-insensitive), by default None
        title : str, optional
            Match publication arxiv id exactly equals this value (case-insensitive), by default None
        _id : str, optional
            Match publication by the provided ID, by default None

        Returns
        -------
        list
            A list of :class:`.Publication` instances
        """

        query = """
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

        variables = {
            'author': author,
            'title': title,
            'id': _id
        }

        result = self.request(query=query, variables=variables)

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

    def create_model(self, name, summary=None, description=None):
        """
        Creates a new model object with the specified parameters.

        Parameters
        ----------
        name : str
            The name of the model to be created
        summary : str, optional
            The summary of the model to be created, by default None
        description : str, optional
            The description of the model to be created, by default None

        Returns
        -------
        Model
            Created Model
        """
        mutation = """
            mutation AddCompasModelMutation($input: AddCompasModelMutationInput!) {
                addCompasModel(input: $input) {
                    id
                }
            }
        """

        params = {
            'input': {
                'name': name,
                'summary': summary,
                'description': description
            }
        }

        result = self.request(mutation, params)

        assert 'id' in result['add_compas_model']

        return self.get_models(_id=result['add_compas_model']['id'])[0]

    @mutually_exclusive('name | summary | description', '_id')
    def get_models(self, name=None, summary=None, description=None, _id=None):
        """
        Fetch all models with name/summary/description containing the values specified.
        Also allows fetching models by the provided ID

        At most, only one of (name, summary, description) or _id must be provided. If no parameter is provided, all
        models are returned.

        Parameters
        ----------
        name : str, optional
            Match model name containing this value (case-insensitive), by default None
        summary : str, optional
            Match model summary contains this value (case-insensitive), by default None
        description : str, optional
            Match model description contains this value (case-insensitive), by default None
        _id : str, optional
            Match model by the provided ID, by default None

        Returns
        -------
        list
            A list of :class:`.Model` instances
        """

        query = """
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

        variables = {
            'name': name,
            'summary': summary,
            'description': description,
            'id': _id
        }

        result = self.request(query=query, variables=variables)

        return [Model(**kw['node']) for kw in result['compas_models']['edges']]

    def delete_model(self, model):
        """
        Delete a model represented by the provided model.

        Parameters
        ----------
        model: Model
            The Model instance to delete
        """

        mutation = """
            mutation DeleteCompasModelMutation($input: DeleteCompasModelMutationInput!) {
                deleteCompasModel(input: $input) {
                    result
                }
            }
        """

        params = {
            'input': {
                'id': model.id
            }
        }

        result = self.request(mutation, params)

        assert result['delete_compas_model']['result']

    def create_dataset(self, publication, model, datafile):
        """
        Creates a new dataset object with the specified publication and model.

        Parameters
        ----------
        publication : Publication
            The Publication this dataset is for
        model : Model
            The model this dataset is for
        datafile : Path
            Local path to the COMPAS dataset file

        Returns
        -------
        Dataset
            Created Dataset
        """
        mutation = """
            mutation AddCompasDatasetModelMutation($input: AddCompasDatasetModelMutationInput!) {
                addCompasDatasetModel(input: $input) {
                    id
                }
            }
        """

        with Path(datafile).open('rb') as f:
            params = {
                'input': {
                    'compas_publication': publication.id,
                    'compas_model': model.id,
                    'file': f
                }
            }

            result = self.request(mutation, params)

        assert 'id' in result['add_compas_dataset_model']

        return self.get_datasets(_id=result['add_compas_dataset_model']['id'])[0]

    @mutually_exclusive('publication | model', '_id')
    def get_datasets(self, publication=None, model=None, _id=None):
        """
        Fetch all dataset models with publication/model matching the provided parameters.
        Also allows fetching models by the provided ID

        At most, only one of (publication, model) or _id must be provided. If no parameter is provided, all
        dataset models are returned.

        Parameters
        ----------
        publication : Publication, optional
            Match all dataset models with this publication, by default None
        model : Model, optional
            Match all dataset models with this publication, by default None
        _id : str, optional
            Match model by the provided ID, by default None

        Returns
        -------
        list
            A list of Dataset instances
        """

        query = """
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

        variables = {
            'publication': publication.id if publication else None,
            'model': model.id if model else None,
            'id': _id
        }

        result = self.request(query=query, variables=variables)

        # Handle publication and model objects
        for dataset in result['compas_dataset_models']['edges']:
            # Handle publication keywords
            dataset['node']['compas_publication']['keywords'] = \
                [Keyword(**kw['node']) for kw in dataset['node']['compas_publication']['keywords']['edges']]

            dataset['node']['publication'] = Publication(**dataset['node']['compas_publication'])
            dataset['node']['model'] = Model(**dataset['node']['compas_model'])

            # Delete the compas_ fields - we don't need them anymore
            del dataset['node']['compas_publication']
            del dataset['node']['compas_model']

        return [Dataset(**kw['node']) for kw in result['compas_dataset_models']['edges']]

    def delete_dataset(self, dataset):
        """
        Delete a dataset represented by the provided dataset.

        Parameters
        ----------
        dataset: Dataset
            The Dataset instance to delete
        """

        mutation = """
            mutation DeleteCompasDatasetModelMutation($input: DeleteCompasDatasetModelMutationInput!) {
                deleteCompasDatasetModel(input: $input) {
                    result
                }
            }
        """

        params = {
            'input': {
                'id': dataset.id
            }
        }

        result = self.request(mutation, params)

        assert result['delete_compas_dataset_model']['result']

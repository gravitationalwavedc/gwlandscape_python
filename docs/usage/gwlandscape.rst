Using the GWLandscape class
===========================

The GWLandscape class will be used to handle all requests to the GWLandscape server.
The public methods of the GWLandscape class are focused on the processes required to upload a dataset, including creating publications and their associated keywords, as well as creating models.
In this tutorial we will walk through the full process to upload a new dataset.

Instantiating
-------------

As discussed in the previous section, we must first instantiate the class with our API token, to authenticate with the GWLandscape service:

::

    from gwlandscape_python import GWLandscape

    gwl = GWLandscape(token='my_unique_gwlandscape_api_token')


Working with keywords
---------------------

Datasets in GWLandscape comprise publications and models. Before we create a publication though, we should have a list of keywords to asign to the publication.
We can browse the available keywords by calling the :meth:`~.GWLandscape.get_keywords` method:

::

    keywords = gwl.get_keywords()

Which returns a list of all available keywords:

::

    >>> for keyword in keywords:
    ...     print(keyword)
    
    Keyword("Binary Neutron Star")
    Keyword("Common Envelope")
    Keyword("Gravitational Waves")



If we wish to obtain just a subset of this list, we can make use of the :code:`exact` or :code:`contains` arguments to match the whole or parts of the tag, or :code:`_id` to match the `id` of the keyword.

In the event that the desired keyword doesn't already exist, we can create a keyword by invoking the :meth:`~.GWLandscape.create_keyword` method:

::

    keyword = gwl.create_keyword('Binary Black Hole')



Creating and browsing publications
----------------------------------

As with the keywords, it is possible to view the existing publications with :meth:`~.GWLandscape.get_publications`:

::

    publications = gwl.get_publications()

which returns a list of :class:`.Publication` objects:

::

    >>> for publication in publications:
    ...     print(publication)

    Publication("Common envelope episodes that lead to double neutron star formation")
    Publication("Formation of the first three gravitational wave observations through isolated binary evolution")
    Publication("On the formation history of galactic double neutron stars")

This method can also take :code:`author` and :code:`title` arguments to filter the returned list, or :code:`_id` to obtain a specific publication by ID.

In the event that our publication does not already exist in the GWLandscape database, we can then use the :meth:`~.GWLandscape.create_publication` method to create it.
At minimum, we'll need the author, title and arXiv ID of the publication, though it is good practice to assign keywords to the publication as well.
We can obtain a list of appropriate keywords using methods in the previous sections.
Alternatively, we can use a list of keyword strings, but if these keywords don't already exist in the system, the method will throw an error.

::

    publication = gwl.create_publication(
        author='Bill Nye',
        title='How gravitational waves prove the Flat Earth model',
        arxiv_id='1234.12345',
        keywords=keywords
    )

This method is also able to take many other arguments to provide information about the created publication.
For the full list of arguments, please see the :meth:`~.GWLandscape.create_publication` documentation.
    

Creating and browsing models
----------------------------

The next step towards creating a new dataset is to create or obtain a model that will be included.
Similar to the publications, we can browse the list of available models with the :meth:`~.GWLandscape.get_models` method:

::

    models = gwl.get_models()

which returns a list of :class:`.Model` objects:

::

    >>> for model in models:
    ...     print(model)

    Model("Fiducial")
    Model("Optimistic CE")

This method takes :code:`name`, :code:`description` and :code:`summary` arguments to filter the list of models, or it can take :code:`_id` to obtain a specific Model by ID.
If we're unable to find the Model to include in our dataset, we can create a new model in a similar fashion to Publications and Keywords.
In this case, the relevant method is :meth:`~.GWLandscape.create_model`:

::

    model = gwl.create_model(name='Pessimistic CE')

We can also supply :code:`description` and :code:`summary` arguments to help further identify the model.


Putting together a dataset
--------------------------

A :class:`.Dataset` object requires a :class:`.Publication`, a :class:`.Model` and the file storing the relevant data.
Before we create a new :class:`.Dataset`, it's pertinent to check if it already exists. Using the :meth:`~.GWLandscape.get_datasets` method, we can obtain a list of all datasets in the system.
However, given that we have a :class:`.Publication` and a :class:`.Model` handy, we can explicitly search the list for any datasets containing these objects:

::

    datasets = gwl.get_datasets(publication=publication, model=model)

If the returned list is empty, we know that our dataset does not already exist, hence we can move onto the creation step.
To create a new dataset on the GWLandscape service, we can use the :meth:`~.GWLandscape.create_dataset` method:

::

    from pathlib import Path

    dataset = gwl.create_dataset(
        publication=publication,
        model=model,
        datafile=Path('/path/to/datafile')


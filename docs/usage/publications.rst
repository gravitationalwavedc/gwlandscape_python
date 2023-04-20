
Creating Publications
=====================

Datasets in GWLandscape comprise publications and models. In this part of the tutorial, we will focus on how to create a new publication.

Browsing publications
---------------------

Perhaps the first step to creating a publication is to check if the publication already exists in the GWLandscape database.
We can browse the list of create publications using :meth:`~.GWLandscape.get_publications`:

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
In the event that our publication does not exist in the database, we can move on to creating it.

Working with keywords
---------------------

It is good practice to assign a list of keywords to the publication as we create it.
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

On the off chance that a keyword has been created with a mistake in the tag, the keyword can be updated with :meth:`.Keyword.update`:

::

    keyword.update(tag='Updated Tag')

Or deleted from the GWLandscape databse with :meth:`.Keyword.delete`.


Creating a publication
----------------------

We have established that our publication doesn't exist, and have obtained a list of existing keywords to be assigned to a new publication.
We can then use the :meth:`~.GWLandscape.create_publication` method to create it.
At minimum, we'll need the author, title and arXiv ID of the publication, though it is good practice to assign keywords to the publication as well.
We can obtain a list of appropriate keywords using methods in the previous section.
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

We are now able to show that our publication is present in the GWLandscape database, by running:

::

    >>> for publication in gwl.get_publications(author="Bill Nye"):
    ...     print(publication)

    Publication("How gravitational waves prove the Flat Earth model")

Updating and deleting publications
----------------------------------

If we accidentally make a mistake with the parameters of our publication, we can update the data using :meth:`.Publication.update`.
For example, if we recall that the full title of our paper is actually something different, we can modify it as follows:

::

    >>> print(publication.title)

    How gravitational waves prove the Flat Earth model

    >>> publication.update(title="How gravitational waves prove the Flat Earth model: evidence from around the globe")
    >>> print(publication.title)

    How gravitational waves prove the Flat Earth model: evidence from around the globe

All parameters of the publication can be updated in this way, except for the creation time and the ID.
Publications may also be removed from the GWLandscape database by calling :meth:`.Publication.delete`.
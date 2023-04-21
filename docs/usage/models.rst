Creating Models
===============

The next step towards creating a new dataset is to create or obtain a model that will be included.

Browsing models
---------------

Similar to the publications and keywords, we can browse the list of available models with the :meth:`~.GWLandscape.get_models` method:

::

    models = gwl.get_models()

which returns a list of :class:`.Model` objects:

::

    >>> for model in models:
    ...     print(model)

    Model("Fiducial")
    Model("Optimistic CE")

This method takes :code:`name`, :code:`description` and :code:`summary` arguments to filter the list of models, or it can take :code:`_id` to obtain a specific model by ID.

Creating models
---------------

If we're unable to find the model to include in our dataset, we can create a new model in a similar fashion to publications and keywords.
In this case, the relevant method is :meth:`~.GWLandscape.create_model`:

::

    model = gwl.create_model(name='Pessimistic CE')

We can also supply :code:`description` and :code:`summary` arguments to help further identify the model.

Updating and deleting models
----------------------------

Similarly to publications, we can update models with the :meth:`.Model.update` method.
For example, in this case, we forgot that we should have added a description to our new model:

::

    >>> model.update(description="A glass half empty kind of CE")
    >>> print(model.description)

    A glass half empty kind of CE

Models can have all of their parameters updated with this method, except for ID.
If necessary, models may also be removed from the GWLandscape database with :meth:`.Model.delete`.
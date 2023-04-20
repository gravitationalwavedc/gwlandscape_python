Putting Together a Dataset
==========================

A :class:`.Dataset` object requires a :class:`.Publication`, a :class:`.Model` and the file storing the relevant data.

Browsing datasets
-----------------

Before we create a new :class:`.Dataset`, it's pertinent to check if it already exists. Using the :meth:`~.GWLandscape.get_datasets` method, we can obtain a list of all datasets in the system.
However, given that we have a :class:`.Publication` and a :class:`.Model` handy, we can explicitly search the list for any datasets containing these objects:

::

    datasets = gwl.get_datasets(publication=publication, model=model)

If the returned list is empty, we know that our dataset does not already exist, hence we can move onto the creation step.

Creating a dataset
------------------

To create a new dataset on the GWLandscape service, we can use the :meth:`~.GWLandscape.create_dataset` method:

::

    from pathlib import Path

    dataset = gwl.create_dataset(
        publication=publication,
        model=model,
        datafile=Path('/path/to/datafile')

Updating and deleting datasets
------------------------------

Given that datasets may often require significant time investment to upload large files, updating the publications and models associated with them is potentially very useful.
We can update the dataset with :meth:`.Dataset.update`:

::

    new_publication = gwl.get_publication(title="On the formation history of galactic double neutron stars")
    dataset.update(publication=new_publication)

Only the publication and model can be updated with this method.
If the data file must be updated, we should instead remove the old dataset with :meth:`.Dataset.delete`, and then create a new dataset with the correct file.

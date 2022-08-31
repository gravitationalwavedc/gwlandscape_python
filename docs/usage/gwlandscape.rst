Using the GWLandscape class
===========================

The GWLandscape class will be used to handle all requests to the GWLandscape server.
The public methods of the GWLandscape class are focused on creating, retrieving and deleting the keywords, publications, models and datasets in the GWLandscape database.
Below we will walk through some of the more common use cases.

Instantiating
-------------

As discussed in the previous section, we must first instantiate the class with our API token, to authenticate with the GWLandscape service:

::

    from gwlandscape_python import GWLandscape

    gwl = GWLandscape(token='my_unique_gwlandscape_api_token')

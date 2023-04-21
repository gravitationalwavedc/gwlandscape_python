The GWLandscape class
=====================

The :class:`.GWLandscape` class will be used to handle all requests to the GWLandscape server.
As discussed in the previous section, we must first instantiate the class with our API token, to authenticate with the GWLandscape service:

::

    from gwlandscape_python import GWLandscape

    gwl = GWLandscape(token='my_unique_gwlandscape_api_token')

The public methods of the GWLandscape class are focused on the processes required to upload a dataset.
This includes creating publications and their associated keywords, as well as creating models.
In this tutorial we will walk through the full process to upload a new dataset.
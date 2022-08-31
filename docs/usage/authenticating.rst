Importing and Authenticating
============================

Almost any script you can write involving the GWLandscape API will require authenticating with the GWLandscape service first.
If you have not yet obtained an API token to authenticate with, read the :ref:`Getting Access <api-token-label>` section first.

::

    from gwlandscape_python import GWLandscape

    gwc = GWLandscape(token='my_unique_gwlandscape_api_token')

An instance of the GWLandscape class initialised with your token will provide an interface to the GWLandscape service, enabling you to manipulate jobs and their results as you might with the GWLandscape UI.
Remember not to share this token with others!

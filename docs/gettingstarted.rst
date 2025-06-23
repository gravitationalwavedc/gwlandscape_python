Getting started with gwlandscape-python
=======================================

Installation
------------

You will require Python 3.7+ to be able to use gwlandscape-python. The recommended way to install gwlandscape-python is with pip:

::

    pip install gwlandscape-python


.. _api-token-label:

Getting Access
--------------

In order to be able to use the gwlandscape-python package, you will need LIGO credentials or a GWLandscape account. You will also need an API Token associated with that account.
You can use your GWLandscape or LIGO account details on the GWLandscape `login page <https://gwlandscape.org.au/sso/login/>`_.


If you don't have an existing GWLandscape account, `register here <https://gwlandscape.org.au/sso/signup/>`_.


Using your GWLandscape or LIGO account, you can generate an `API token <https://gwlandscape.org.au/api-token>`_.
You should be greeted with a page which has a "Create Token" button. If you click on this, a new, unique API token will be generated.
Note that this is the only time the token will be visible.
Press the "Copy" button to copy the token to your clipboard.


An API token operates as your credentials, replacing your username and password when using the API.
You are also able to revoke your token at any point by clicking the "Revoke Token" button, at which point the token will cease to function.
You must not share it with anybody and should revoke and recreate it if somebody else obtains it.

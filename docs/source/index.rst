.. socketsc documentation master file, created by
   sphinx-quickstart on Mon Nov 28 14:57:24 2022.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

socketsc
====================================

.. image:: https://img.shields.io/pypi/l/socketsc
   :target: https://pypi.org/project/socketsc/
   :alt: PyPI - License

.. image:: https://img.shields.io/pypi/v/socketsc
   :target: https://pypi.org/project/socketsc/
   :alt: PyPi - Version

.. image:: https://img.shields.io/pypi/pyversions/socketsc
   :target: https://pypi.org/project/socketsc/
   :alt: PyPI - Python Version

.. image:: https://img.shields.io/pypi/dm/socketsc
   :target: https://pypi.org/project/socketsc/
   :alt: PyPI - Downloads

.. image:: https://img.shields.io/gitlab/issues/open/dan5py/socketsc
   :target: https://gitlab.com/dan5py/socketsc/-/issues
   :alt: GitLab issues


.. toctree::
   :maxdepth: 2
   :caption: Contents:

.. warning::

   This is a work in progress. The API is not stable and may change at any time.

:mod:`socketsc` is a Python library for creating socket clients and servers.
It features an events management system that allows you to easily create and handle events both on the client and server side.

Example of a simple client:

.. literalinclude:: ../../example/client.py


And a simple server:

.. literalinclude:: ../../example/server.py


.. toctree::
   :hidden:

   getting-started/index
   references/index
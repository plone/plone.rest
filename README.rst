.. image:: https://secure.travis-ci.org/plone/plone.rest.png?branch=master
  :target: http://travis-ci.org/plone/plone.rest

.. image:: https://coveralls.io/repos/plone/plone.rest/badge.png?branch=master
  :target: https://coveralls.io/r/plone/plone.rest

.. image:: https://landscape.io/github/plone/plone.rest/master/landscape.svg?style=plastic
  :target: https://landscape.io/github/plone/plone.rest/master
  :alt: Code Health

.. image:: https://img.shields.io/pypi/dm/plone.rest.svg
    :target: https://pypi.python.org/pypi/plone.rest/
    :alt: Downloads

.. image:: https://img.shields.io/pypi/v/plone.rest.svg
    :target: https://pypi.python.org/pypi/plone.rest/
    :alt: Latest Version

.. image:: https://img.shields.io/pypi/status/plone.rest.svg
    :target: https://pypi.python.org/pypi/plone.rest/
    :alt: Egg Status

.. image:: https://img.shields.io/pypi/l/plone.rest.svg
    :target: https://pypi.python.org/pypi/plone.rest/
    :alt: License


==========
Plone REST
==========

Purpose
-------

plone.rest allows you to use HTTP verbs such as GET, POST, PUT, DELETE, etc. in `Plone <https://www.plone.org>`_.

REST stands for `Representational State Transfer <http://en.wikipedia.org/wiki/Representational_state_transfer>`_.
It is a software architectural principle to create loosely coupled web APIs.

plone.rest provides the basic infrastructure that allows us to build RESTful endpoints in Plone.

The reason for separating this infrastructure into a separate package from the 'main' full `Plone REST API <https://github.com/plone/plone.restapi>`_ is so you can create alternative endpoints tailored to specific usecases. A number of these specific endpoints are already in active use.


Audience
--------

plone.rest is for experienced web developers who want to build their own HTTP/REST endpoints on top of Plone.

If you want to **use** a ready-made full RESTful Plone API, you should use `plone.restapi <https://github.com/plone/plone.restapi>`_.
That package uses, and depends upon, this one.


Features
--------

* Registering RESTful service endpoints for the following HTTP verbs:

  * GET
  * POST
  * PUT
  * DELETE
  * PATCH
  * OPTIONS

* Support for Dexterity and Archetypes-based content objects
* Content negotiation ('application/json' is currently the only format supported).
* Named services allows to register service endpoints for custom URLs


Registering RESTful Service Endpoints
-------------------------------------

plone.rest allows you to register HTTP verbs for Plone content with ZCML.

This is how you would register a PATCH request on Dexterity content:

.. code-block:: xml

  <plone:service
    method="PATCH"
    for="plone.dexterity.interfaces.IDexterityContent"
    factory=".service.Patch"
    />

You have to specify the HTTP verb (GET, POST, PUT, DELETE, HEAD, OPTIONS), the interface for the content objects and the factory class that actually returns the content.

The factory class needs to inherit from the plone.rest 'Service' class and to implement a render method that returns a list or a dict::

  from plone.rest import Service

  class Patch(Service):

      def render(self):
          return {'message': 'PATCH: Hello World!'}


The return value (list or dict) will be automatically transformed into JSON.


Content Negotiation
-------------------

To access the service endpoint we just created we have to send a GET request to a Dexterity object by setting the 'Accept' header to 'application/json'::

  PATCH /Plone/doc1 HTTP/1.1
  Host: localhost:8080
  Accept: application/json

The server then will respond with '200 OK'::

  HTTP/1.1 200 OK
  Content-Type: application/json

  {
    'message': 'PATCH: Hello World!'
  }

You can try this out on the command line:

.. code-block:: console

    $ http --auth admin:admin PATCH localhost:8080/Plone/doc1 Accept:application/json

.. note:: You have to install httpie (pip install httpie) to make this example work.

Here is a list of examples for all supported HTTP verbs:

GET::

  $ http --auth admin:admin GET localhost:8080/Plone/doc1 Accept:application/json

POST::

  $ http --auth admin:admin POST localhost:8080/Plone/doc1 Accept:application/json

PUT::

  $ http --auth admin:admin PUT localhost:8080/Plone/doc1 Accept:application/json

DELETE::

  $ http --auth admin:admin DELETE localhost:8080/Plone/doc1 Accept:application/json

PATCH::

  $ http --auth admin:admin PATCH localhost:8080/Plone/doc1 Accept:application/json

OPTIONS::

  $ http --auth admin:admin OPTIONS localhost:8080/Plone/doc1 Accept:application/json


If you want to use any other accept header you can define on the service, actual implementation will make all requests with that verb and accept header be treated as APIRequests::

  <plone:service
    method="POST"
    for="plone.dexterity.interfaces.IDexterityContent"
    factory=".demo.NamedGet"
    name="negotiation_no_wildcard"
    accept="text/html,application/json"/>

  <plone:service
    method="GET"
    for="plone.dexterity.interfaces.IDexterityContent"
    factory=".demo.NamedGet"
    name="negotiation_open_wildcard"
    accept="*/*"/>

ALERT: Right now when you define an accept header for the service it will be applied to all services with the same method.

Named Services
--------------

Named services can be registered by providing a 'name' attribute in the service directive:

.. code-block:: xml

  <plone:service
    method="GET"
    for="Products.CMFPlone.interfaces.IPloneSiteRoot"
    factory=".service.Search"
    name="search"
    />

This registers a service endpoint accessible at the site root using the
following request::

  GET /Plone/search HTTP/1.1
  Host: localhost:8080
  Accept: application/json

CORS
----

By default CORS to all hosts is enabled to API REST calls. You can define them on the Service definition

.. code-block:: xml

  <plone:service
    method="POST"
    for="plone.dexterity.interfaces.IDexterityContent"
    factory=".factory.Factory"
    name="corsexample"
    cors_origin="foobar"
    cors_max_age="33400"
    cors_expose_all_headers="yes"
    cors_auth="yes"
    cors_headers="X-MYHEADER"
    cors_enabled="yes"
    />

cors_origin::

  The list of origins for CORS. You can use wildcards here if needed, e.g. 'list', 'of', '*.domain'
  Default : '*'

cors_enabled::

  To use if you especially want to disable CORS support for a particular service / method.
  Default: 'yes'

cors_headers::

  The list of headers supported for the services
  Default: None

cors_auth::

  Accept Authentication headers on CORS
  Default: 'yes'

cors_expose_all_headers::

  If set to True, all the headers will be exposed and considered valid ones (Default: True). If set to False, all the headers need be explicitly mentioned with the cors_headers parameter.
  Default: 'yes'

cors_max_age::

  Indicates how long the results of a preflight request can be cached in a preflight result cache
  Default: None

Installation
------------

Install plone.rest by adding it to your buildout::

   [buildout]

    ...

    eggs =
        plone.rest

and then running "bin/buildout"


Contribute
----------

- Issue Tracker: https://github.com/plone/plone.rest/issues
- Source Code: https://github.com/plone/plone.rest
- Documentation: https://pypi.python.org/pypi/plone.rest


Support
-------

This package is maintained by Timo Stollenwerk <tisto@plone.org> and Ramon Navarro Bosch <ramon.nb@gmail.com>.

If you are having issues, please `let us know <https://github.com/plone/plone.rest/issues>`_.


License
-------

The project is licensed under the GPLv2.

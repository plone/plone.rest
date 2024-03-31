.. image:: https://github.com/plone/plone.rest/actions/workflows/tests.yml/badge.svg
   :alt: Github Actions Status
   :target: https://github.com/plone/plone.rest/actions/workflows/tests.yml

.. image:: https://img.shields.io/coveralls/github/plone/plone.rest.svg
   :alt: Coveralls github
   :target: https://coveralls.io/github/plone/plone.restapi

.. image:: https://img.shields.io/pypi/status/plone.rest.svg
    :target: https://pypi.org/project/plone.rest/
    :alt: Egg Status

.. image:: https://img.shields.io/pypi/v/plone.rest.svg
    :target: https://pypi.org/project/plone.rest/
    :alt: Latest Version

.. image:: https://img.shields.io/pypi/l/plone.rest.svg
    :target: https://pypi.org/project/plone.rest/
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

The reason for separating this infrastructure into a separate package from the 'main' full `Plone REST API <https://github.com/plone/plone.restapi>`_ is so you can create alternative endpoints tailored to specific usecases.
A number of these specific endpoints are already in active use.


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
* Content negotiation: Services can be registered for arbitrary media types (e.g. 'application/json').
* Named services allows to register service endpoints for custom URLs


Registering RESTful Service Endpoints
-------------------------------------

plone.rest allows you to register HTTP verbs for Plone content with ZCML.

This is how you would register a PATCH request on Dexterity content:

.. code-block:: XML

  <plone:service
    method="PATCH"
    accept="application/json"
    for="plone.dexterity.interfaces.IDexterityContent"
    factory=".service.Patch"
    permission="cmf.ModifyPortalContent"
    />

You have to specify the HTTP verb (GET, POST, PUT, DELETE, HEAD, OPTIONS), the
media type used for content negotiation, the interface for the content objects,
the factory class that actually returns the content and the permission required
to access the service.

The factory class needs to inherit from the plone.rest 'Service' class and to implement a render method that returns the body of the response::

  from plone.rest import Service

  class Patch(Service):

      def render(self):
          return '{"message": "PATCH: Hello World!"}'


Content Negotiation
-------------------

To access the service endpoint we created we have to send a GET request to a Dexterity object:

1. by setting the 'Accept' header to 'application/json'::

    PATCH /Plone/doc1 HTTP/1.1
    Host: localhost:8080
    Accept: application/json

2. or by adding an explicit traversal step to the path like so::

    PATCH /Plone/++api++/doc1 HTTP/1.1
    Host: localhost:8080

The server then will respond with '200 OK'::

  HTTP/1.1 200 OK
  Content-Type: application/json

  {
    "message": "PATCH: Hello World!"
  }

Why two methods?
Using the 'Accept' header is the intended way of RESTful APIs to get different responses from the same URL.
However, if it comes to caching the response in an web accelerator like Varnish or Cloudflare, additional challenges are added.
Setting the `Vary` header to 'Vary: Accept' helps to a certain degree in Varnish.
But cache pollution may happen, because different browsers send different headers on normal HTML requests.
Hosted services like Cloudflare just do not support the 'Vary' usage and can not be used for sites with REST calls.
Thus a second option with different URLs is needed.


You can try this out on the command line:

.. code-block:: console

    $ http --auth admin:admin PATCH localhost:8080/Plone/doc1 Accept:application/json

.. note:: You have to install httpie (pip install httpie) to make this example work.

Here is a list of examples for all supported HTTP verbs:

GET::

  $ http --auth admin:admin GET localhost:8080/Plone/doc1 Accept:application/json
  $ http --auth admin:admin GET localhost:8080/Plone/++api++/doc1

POST::

  $ http --auth admin:admin POST localhost:8080/Plone/doc1 Accept:application/json
  $ http --auth admin:admin POST localhost:8080/Plone/++api++/doc1

PUT::

  $ http --auth admin:admin PUT localhost:8080/Plone/doc1 Accept:application/json
  $ http --auth admin:admin PUT localhost:8080/Plone/++api++/doc1

DELETE::

  $ http --auth admin:admin DELETE localhost:8080/Plone/doc1 Accept:application/json
  $ http --auth admin:admin DELETE localhost:8080/Plone/++api++/doc1

PATCH::

  $ http --auth admin:admin PATCH localhost:8080/Plone/doc1 Accept:application/json
  $ http --auth admin:admin PATCH localhost:8080/Plone/++api++/doc1

OPTIONS::

  $ http --auth admin:admin OPTIONS localhost:8080/Plone/doc1 Accept:application/json
  $ http --auth admin:admin OPTIONS localhost:8080/Plone/++api++/doc1


Named Services
--------------

Named services can be registered by providing a 'name' attribute in the service directive:

.. code-block:: XML

  <plone:service
    method="GET"
    accept="application/json"
    for="Products.CMFPlone.interfaces.IPloneSiteRoot"
    factory=".service.Search"
    name="search"
    permission="zope2.View"
    />

This registers a service endpoint accessible at the site root using the
following request::

  GET /Plone/search HTTP/1.1
  Host: localhost:8080
  Accept: application/json

Service endpoints can also be accessed using the traverser::

  GET /Plone/++api++/search HTTP/1.1
  Host: localhost:8080


Additional Path Segments
------------------------

To handle additional path segments after the service url like `/Plone/myservice/1/2`
a service has to implement `IPublishTraverse`. The following example simply
stores all path segments in an array in `self.params`.

.. code-block:: python

  from plone.rest import Service
  from zope.interface import implementer
  from zope.publisher.interfaces import IPublishTraverse

  @implementer(IPublishTraverse)
  class MyService(Service):

      def __init__(self, context, request):
          super(MyService, self).__init__(context, request)
          self.params = []

      def publishTraverse(self, request, name):
          self.params.append(name)
          return self

      def render(self):
          return {'service': 'named get', 'params': self.params}


See also the implementation of the workflow transition endpoint in
plone.restapi for an other example.


CORS
----

plone.rest allows you to define CORS policies for services in ZCML. The
following example defines a policy for all services.

.. code-block:: XML

  <plone:CORSPolicy
    allow_origin="http://example.net"
    allow_methods="DELETE,GET,OPTIONS,PATCH,POST,PUT"
    allow_credentials="true"
    expose_headers="Content-Length,X-My-Header"
    allow_headers="Accept,Authorization,Content-Type,X-Custom-Header"
    max_age="3600"
    />

CORS policies can be bound to specific interfaces of content objects and to
specific browser layers. This allows us to define different policies for
different content types or to override existing policies. The following example
defines a policy for the site root.

.. code-block:: XML

  <plone:CORSPolicy
    for="Products.CMFPlone.interfaces.IPloneSiteRoot"
    layer="myproduct.interfaces.IMyBrowserLayer"
    allow_origin="*"
    allow_methods="GET"
    />

The CORSPolicy directive supports the following options:

allow_origin
  Origins that are allowed to access the resource. Either a comma separated
  list of origins, e.g. "http://example.net,http://mydomain.com" or "*".

allow_methods
  A comma separated list of HTTP method names that are allowed by this CORS
  policy, e.g. "DELETE,GET,OPTIONS,PATCH,POST,PUT". If not specified, all
  methods for which there's a service registered are allowed.

allow_credentials
  Indicates whether the resource supports user credentials in the request.

allow_headers
  A comma separated list of request headers allowed to be sent by the client,
  e.g. "X-My-Header"

expose_headers
  A comma separated list of response headers clients can access,
  e.g. "Content-Length,X-My-Header".

max_age
  Indicates how long the results of a preflight request can be cached.

for
  Specifies the interface for which the CORS policy is registered. If this
  attribute is not specified, the CORS policy applies to all objects.

layer
  A browser layer for which this CORS policy is registered. Useful for
  overriding existing policies or for making them available only if a specific
  add-on has been installed.


Installation
------------

Install plone.rest by adding it to your buildout::

   [buildout]

    ...

    eggs =
        plone.rest

and then running "bin/buildout"


Plone/Python Support
--------------------

plone.rest 4.x.x supports Plone 5.2 and 6.x on Python 3.8 and newer.

plone.rest 3.x.x supports Plone 5.2 on Python 2.7 and 3.6 to 3.8 and Plone 6.0 on Python 3.8 to 3.11.

If you need to use Plone 4.3, 5.0, or 5.1 on Python 2.7, check out plone.rest 2.x.x or 1.x.x.

Redirects
---------

plone.rest will handle redirects created by ``plone.app.redirector`` pretty
much the same way as regular Plone.

If a redirect exists for a given URL, a ``GET`` request will be answered with
``302``, and the new location for the resource is indicated in the ``Location``
header::

  HTTP/1.1 302 Moved Temporarily

  Content-Type: application/json
  Location: http://localhost:8080/Plone/my-folder-new-location

Any other request method than GET (``POST``, ``PATCH``, ...) will be answered
with ``307 Temporary Redirect``. This status code instructs the client that
it should NOT switch the method, but retry (if desired) the request with the
*same* method at the new location.

In practice, both the Python ``requests`` library a well as Postman seem to
honour this behavior by default.


Contribute
----------

- Issue Tracker: https://github.com/plone/plone.rest/issues
- Source Code: https://github.com/plone/plone.rest
- Documentation: https://pypi.org/project/plone.rest/


Support
-------

This package is maintained by Timo Stollenwerk <tisto@plone.org>.

If you are having issues, please `let us know <https://github.com/plone/plone.rest/issues>`_.


Credits
-------

plone.rest has been written by Timo Stollenwerk (`kitconcept GmbH <http://kitconcept.com>`_) and Ramon Navarro Bosch (`Iskra <https://iskra.cat>`_).

plone.rest was added as a Plone core package with Plone 5.2 (see `<https://github.com/plone/Products.CMFPlone/issues/2177>`_).


License
-------

The project is licensed under the GPLv2.

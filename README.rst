==========
Plone REST
==========

Purpose
-------

plone.rest allows you to use HTTP verbs such as GET, POST, PUT, DELETE, etc. in `Plone <https://www.plone.org>`_.

REST stands for `Representational State Transfer <http://en.wikipedia.org/wiki/Representational_state_transfer>`_.
It is a software architectural principle to create loosely coupled web APIs.

plone.rest provides the basic infrastructure that allows us to build RESTful endpoints in Plone.

The reason for separating this infrastructure into a separate package from the 'main' full `Plone REST API <https://github.com/plone/plone.restapi>`_ is so you can create alternative endpoints tailored to specific usecases. A number of these specific end points are already in active use.


Audience
--------

plone.rest is for experienced web developers who want to build their own endpoints on top of Plone.

If you want to **use** a ready-made full RESTful Plone API, you should use `plone.restapi <https://github.com/plone/plone.restapi>`_.
That package uses, and depends upon, this one.


Features
--------

plone.rest currently supports the following HTTP verbs:

* GET
* POST
* PUT
* DELETE
* PATCH
* OPTIONS

Those verbs can be registered for Dexterity content objects and the Plone site root. The only format that is currently supported via HTTP content negotiation is 'application/json'.


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

  http --auth admin:admin DELETE localhost:8080/Plone/doc1 Accept:application/json

PATCH::

  http --auth admin:admin PATCH localhost:8080/Plone/doc1 Accept:application/json

OPTIONS::

  http --auth admin:admin OPTIONS localhost:8080/Plone/doc1 Accept:application/json


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


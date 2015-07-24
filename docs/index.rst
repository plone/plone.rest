========================
plone.rest documentation
========================


Registering RESTful Service Endpoints
-------------------------------------

plone.rest allows you to register HTTP verbs for Plone content with ZCML.

This is how you would register a PATCH request on Dexterity content:

.. code-block:: xml

  <plone:service
    method="PATCH"
    for="plone.dexterity.interfaces.IDexterityContent"
    factory=".service.PATCH"
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

Here is a list of examples for all HTTP verbs.

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
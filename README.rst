Plone REST
==========

plone.rest provides the basic infrastructure to register RESTful service endpoints on top of existing Plone content.

Service consumers can access Plone content by using content negotiation and standard HTTP verbs such as (GET, POST, PUT, DELETE, etc.).

..note::
  If you are looking for a full RESTful Plone API, please have a look at plone.restapi.


Registering RESTful Service Endpoints
-------------------------------------

plone.rest allows you to register HTTP verbs on top of existing Plone content with ZCML::

  <plone:service
    method="GET"
    for="plone.dexterity.interfaces.IDexterityContent"
    factory=".service.Get"
    />

The service class needs to inherit from the plone.rest Service class and implement a render method that returns a list or a dict::

  from plone.rest import Service

  class Get(Service):

      def render(self):
          return {'message': 'GET: Hello World!'}


Content Negotiation
-------------------

You can access the service endpoint we just created by sending a GET request to a Dexterity object and set the 'Accept' header to 'application/json'::

  GET /my-document HTTP/1.1
  Host: localhost:8080
  Accept: application/json

Command Line::

  $ http --auth admin:admin GET localhost:8080/Plone/document1 Accept:application/json

The server then will respond with '200 OK'::

  HTTP/1.1 200 OK
  Content-Type: application/json

  {
    'message': 'GET: Hello World!'
  }

HTTP Verbs
----------

plone.rest currently support the following HTTP verbs::

* GET
* POST
* PUT
* DELETE
* PATCH
* OPTIONS

See events.py for more details. If there are verbs missing, feel free to open an issue and we will add support for additional verbs.

GET::

  $ http --auth admin:admin GET localhost:8080/Plone Accept:application/json

POST::

  $ http --auth admin:admin POST localhost:8080/Plone Accept:application/json


PUT::

  $ http --auth admin:admin PUT localhost:8080/Plone Accept:application/json


DELETE::

  http --auth admin:admin DELETE localhost:8080/Plone Accept:application/json


Plone Portal Root
-----------------

In addition to Dexterity content objects it is also possible to register service endpoints on the Plone portal root::

  <plone:service
    method="GET"
    for="Products.CMFPlone.interfaces.IPloneSiteRoot"
    factory=".service.Get"
    />

service.py::

  class Get(Service):

      def render(self):
          return {'message': 'GET: Hello Plone Portal Root!'}

Request::

  GET / HTTP/1.1
  Host: localhost:8080
  Accept: application/json

Command Line::

  $ http --auth admin:admin GET localhost:8080/Plone

The server then will respond with '200 OK'::

  HTTP/1.1 200 OK
  Content-Type: application/json

  {
    'message': 'GET: Hello Plone Portal Root!'
  }


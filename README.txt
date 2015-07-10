Plone Portal Root
-----------------

GET::

  $ http --auth admin:admin GET localhost:8080/Plone Content-Type:application/json

  => 404 HTML

POST::

  $ http --auth admin:admin POST localhost:8080/Plone Content-Type:application/json

  => 404 HTML


PUT::

  $ http --auth admin:admin PUT localhost:8080/Plone Content-Type:application/json

  HTTP/1.1 200 OK
  Content-Length: 18
  Content-Type: application/json
  Date: Thu, 09 Jul 2015 14:50:40 GMT
  Server: Zope/(2.13.22, python 2.7.6, linux2) ZServer/1.1

  {
      "service": "put"
  }

DELETE::

  http --auth admin:admin DELETE localhost:8080/Plone Content-Type:application/json

  HTTP/1.1 200 OK
  Content-Length: 21
  Content-Type: application/json
  Date: Thu, 09 Jul 2015 14:51:27 GMT
  Server: Zope/(2.13.22, python 2.7.6, linux2) ZServer/1.1

  {
      "service": "delete"
  }


Plone Content Object
--------------------

All calls return 404 HTML.


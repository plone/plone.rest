==========
Plone REST
==========

Purpose
-------

plone.rest allows you to use HTTP verbs such as GET, POST, PUT, DELETE, etc. in `Plone <https://www.plone.org>`_.

REST stands for `Representational State Transfer <http://en.wikipedia.org/wiki/Representational_state_transfer>`_.
It is a software architectural principle to create loosely coupled web APIs.

plone.rest provides the basic infrastructure that allows us to build RESTful endpoints on top of it.

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

Those verbs can be registered for Dexterity content objects and the Plone site root.
The only format that is currently supported via HTTP content negotiation is 'application/json'.


Full options
------------

Please see the `docs <https://github.com/plone/plone.rest/tree/master/docs>`_ folder.


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


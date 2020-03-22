Changelog
=========

.. You should *NOT* be adding new change log entries to this file.
   You should create a file in the news directory instead.
   For helpful instructions, please see:
   https://github.com/plone/plone.releaser/blob/master/ADD-A-NEWS-ITEM.rst

.. towncrier release notes start

1.6.1 (2020-03-22)
------------------

Bug fixes:


- CORS preflight should happen for all error codes, fixes #101
  [sneridagh] (#101)


1.6.0 (2019-10-15)
------------------

New features:


- Remove CMFPlone and make plone.app.redirector dependency optional [timo] (#81)


1.5.1 (2019-10-15)
------------------

- Brown bag release.


1.5.0 (2019-10-13)
------------------

- Brown bag release.


1.4.0 (2018-11-08)
------------------

New features:

- Python 3 compatibility
  [tschorr,pbauer,frapell]


1.3.0 (2018-09-11)
------------------

New features:

- Remove unnecessary dependency on Products.CMFPlone.
  Import ISiteRoot from Products.CMFCore.interfaces instead of
  IPloneSiteRoot from Products.CMFPlone.interfaces.siteroot.
  [jordic]


1.2.0 (2018-06-29)
------------------

New features:

- Add support for redirects from plone.app.redirector.
  [lgraf]


1.1.1 (2018-06-22)
------------------

Bugfixes:

- Re-release 1.1.0.


1.1.0 (2018-06-22)
------------------

New features:

- Get rid of Products.Five.metaclass dependency for Zope 4 compatibility.
  [timo]


1.0.0 (2018-01-17)
------------------

New features:

- Add support for Plone 5.1.
  [timo]

- Add Plone 4.3, 5.0 and 5.1 to list classifiers in setup.py.
  [timo]

- Set development status to production/stable in setup.py.
  [timo]


1.0b1 (2017-05-14)
------------------

Bugfixes:

- Do not render service in preflight requests when no CORS policy was defined.
  Fixes: https://github.com/plone/plone.rest/issues/63
  [buchi]


1.0a7 (2016-11-21)
------------------

Bugfixes:

- Do not handle view namespace at all. This fixes: https://github.com/plone/plone.rest/issues/50
  [buchi]


1.0a6 (2016-05-22)
------------------

- Add support for CORS policies.
  [buchi]

- Remove JSON render implementation in service base class. Services
  must provide their own render implementation.
  [buchi]

- Fallback to regular views during traversal to ensure compatibility with
  views beeing called with a specific Accept header.
  [buchi]


1.0a5 (2016-02-27)
------------------

- Implement permission handling. The permission required to access a service
  must be declared in the service directive.
  [buchi]

- Register services with the Zope configuration system. This provides better
  conflict detection and resolution.
  [buchi]

- Improve message for 404 Not Found exceptions (don't return HTML).
  [lgraf]

- Add regression tests for service dispatching.
  [lgraf]

- Restrict traversal of REST requests to content objects. This allows us to
  override existing views with a named service (e.g. /search).
  [buchi]

- Allow virtual hosting scenarios. This fixes #48.
  [tomgross]


1.0a4 (2016-02-07)
------------------

- Refactor Dexterity tests to make sure services return the correct object.
  [timo]

- Add support for browser layers. REST services can now be registered to a
  specific browser layer using the 'layer' attribute.
  [buchi]

- Remove request method specific marker interfaces (IGET, IPOST, etc.) because
  they're no longer required for service lookup.
  [buchi]

- Add support for content negotiation. REST services are no longer hardwired
  to 'application/json' Accept headers. Instead the media type can be
  configured with the service directive.
  [buchi]

- Refactor traversal of REST requests by using a traversal adapter on the site
  root instead of a traversal adapter for each REST service. This prevents
  REST services from being overriden by other traversal adapters.
  [buchi]


1.0a3 (2015-12-16)
------------------

- Release fix. 1.0a2 was a brown-bag release. This fixes https://github.com/plone/plone.rest/issues/34.
  [timo]


1.0a2 (2015-12-10)
------------------

- Simplify patch of DynamicType pre-traversal hook and actually make it work
  with Archetypes.
  [buchi]

- Render errors as JSON.
  [jone]

- Add support for named services which allows registering services like
  ``GET /Plone/search`` or ``GET /Plone/doc1/versions/1`` using a 'name' attribute.
  [jone, lukasgraf, buchi]

- Remove "layer" from service directive for now,
  because it is not yet implemented properly.
  [jone]


1.0a1 (2015-08-01)
------------------

- Initial release.
  [bloodbare, timo]

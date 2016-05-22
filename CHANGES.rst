Changelog
=========

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

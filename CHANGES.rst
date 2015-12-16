Changelog
=========

1.0a3 (unreleased)
------------------

- Release fix. 1.0a2 was a brown-bag release. This fixes https://github.com/plone/plone.rest/issues/34.


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

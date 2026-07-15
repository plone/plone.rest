"""Customized implementation of plone.app.caching.lookup.ContentItemLookup for plone.restapi Services"""

from plone.app.caching.interfaces import IPloneCacheSettings
from plone.app.caching.lookup import ContentItemLookup
from plone.caching.interfaces import IRulesetLookup
from plone.registry.interfaces import IRegistry
from zope.component import queryUtility
from zope.interface import implementer


@implementer(IRulesetLookup)
class RestContentItemLookup(ContentItemLookup):
    """General lookup for RestAPI Services.

    1. Look up the published name in the page template mapping (as
       PageTemplateLookup does now) and return that if found

    2. Attempt to look up a ruleset using z3c.caching.registry.lookup()
       and return that if found (this is necessary because this adapter will
       override the default lookup in most cases).

    3. Get the name of the published object (i.e. the name of the view or
       page template).

    4. Find the parent of the published object, possibly a content object.

       4.1. If the parent is a content object:
       4.1.1. Get the default view of the parent content object
       4.1.2. If the name of the published object is the same as the default
              view of the parent:
       4.1.2.1. Otherwise, look up the parent type in the content type mapping
                and return that if found
       4.1.2.2. Look up a ruleset on the parent object and return if that
                matches
    """

    def __call__(self):
        registry = queryUtility(IRegistry)

        if registry is None:
            return

        ploneCacheSettings = registry.forInterface(IPloneCacheSettings, check=False)

        # 2. Get the name of the published object
        name = getattr(self.published, "__name__", None)

        if name is None:
            return

        # 3. Look up the published name in the page template mapping
        ruleset = (
            ploneCacheSettings.templateRulesetMapping
            and ploneCacheSettings.templateRulesetMapping.get(name, None)
        ) or None
        if ruleset is not None:
            return ruleset

        return super().__call__()

try:
    from plone.base.interfaces import INavigationRoot  # noqa
    from plone.base.interfaces import IPloneSiteRoot  # noqa
except ImportError:
    from plone.app.layout.navigation.interfaces import INavigationRoot  # noqa
    from Products.CMFPlone.interfaces import IPloneSiteRoot  # noqa

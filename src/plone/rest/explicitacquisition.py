from zope.component import adapter
from plone.rest.interfaces import IShouldAllowAcquiredItemPublication
from plone.rest.traverse import RESTWrapper


@adapter(RESTWrapper)
def rest_allowed(wrapper):
    return IShouldAllowAcquiredItemPublication(wrapper.context)

from plone.rest.interfaces import IShouldAllowAcquiredItemPublication
from plone.rest.traverse import RESTWrapper
from zope.component import adapter


@adapter(RESTWrapper)
def rest_allowed(wrapper):
    return IShouldAllowAcquiredItemPublication(wrapper.context)

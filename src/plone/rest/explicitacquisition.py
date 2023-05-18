from zope.component import adapter
from Products.CMFCore.interfaces import IShouldAllowAcquiredItemPublication
from plone.rest.traverse import RESTWrapper


@adapter(RESTWrapper)
def rest_allowed(wrapper):
    return IShouldAllowAcquiredItemPublication(wrapper.context)

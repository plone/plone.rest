from zope.component import adapter
from Products.CMFCore.interfaces import IExplicitAcquisitionPublishingAllowed
from plone.rest.traverse import RESTWrapper


@adapter(RESTWrapper)
def rest_allowed(wrapper):
    return IExplicitAcquisitionPublishingAllowed(wrapper.context)

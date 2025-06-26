from plone.rest.interfaces import IAPIRequest
from zope.component import adapter
from zope.component.hooks import getSite
from ZPublisher.interfaces import IPubAfterTraversal


@adapter(IPubAfterTraversal)
def after_traversal_hook(event):
    request = event.request
    if not IAPIRequest.providedBy(request):
        return
    site = getSite()
    if site is not None:
        request["VirtualRootPhysicalPath"] = site.getPhysicalPath()
        _physicalPathToURL = request.physicalPathToURL

        def physicalPathToURL(path, relative=1):
            return _physicalPathToURL(path, relative)

        request.physicalPathToURL = physicalPathToURL

from plone.rest.events import mark_as_api_request
from plone.rest.interfaces import IAPIRequest
from plone.rest.interfaces import IService
from Products.CMFCore.interfaces import IContentish
from Products.CMFCore.interfaces import ISiteRoot
from Products.SiteAccess.VirtualHostMonster import VirtualHostMonster
from zExceptions import Redirect
from zope.component import adapter
from zope.component import queryMultiAdapter
from zope.interface import implementer
from zope.publisher.interfaces.browser import IBrowserPublisher
from zope.traversing.interfaces import ITraversable
from ZPublisher.BaseRequest import DefaultPublishTraverse


@adapter(ISiteRoot, IAPIRequest)
class RESTTraverse(DefaultPublishTraverse):
    def publishTraverse(self, request, name):
        try:
            obj = super().publishTraverse(request, name)
            if not IContentish.providedBy(obj) and not IService.providedBy(obj):
                if isinstance(obj, VirtualHostMonster):
                    return obj
                else:
                    raise KeyError
        except KeyError:
            # No object, maybe a named rest service
            service = queryMultiAdapter(
                (self.context, request), name=request._rest_service_id + name
            )
            if service is None:
                # No service, fallback to regular view
                view = queryMultiAdapter((self.context, request), name=name)
                if view is not None:
                    return view
                raise
            return service

        if name.startswith(request._rest_service_id):
            return obj

        # Do not handle view namespace
        if "@@" in request["PATH_INFO"] or "++view++" in request["PATH_INFO"]:
            return obj

        # Wrap object to ensure we handle further traversal
        return RESTWrapper(obj, request)

    def browserDefault(self, request):
        # Called when we have reached the end of the path
        # In our case this means an unnamed service
        return self.context, (request._rest_service_id,)


@implementer(ITraversable)
class MarkAsRESTTraverser:
    """
    Traversal adapter for the ``++api++`` namespace.
    It marks the request as API request.
    """

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def traverse(self, name_ignored, subpath_ignored):
        name = "/++api++"
        url = self.request.ACTUAL_URL
        if url.count(name) > 1:
            # Redirect to proper url.
            while f"{name}{name}" in url:
                url = url.replace(f"{name}{name}", name)
            if url.count(name) > 1:
                # Something like: .../++api++/something/++api++
                # Return nothing, so a NotFound is raised.
                return
            # Raise a redirect exception to stop execution of the current request.
            raise Redirect(url)
        mark_as_api_request(self.request, "application/json")
        return self.context


@implementer(IBrowserPublisher)
class RESTWrapper:
    """A wrapper for objects traversed during a REST request."""

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self._bpth_called = False

    def __getattr__(self, name):
        # Delegate attribute access to the wrapped object
        # Needed for security checks in ZPublisher traversal
        return getattr(self.context, name)

    def __getitem__(self, name):
        # Delegate key access to the wrapped object
        return self.context[name]

    # MultiHook requires this to be a class attribute
    def __before_publishing_traverse__(self, arg1, arg2=None):
        bpth = getattr(self.context, "__before_publishing_traverse__", False)
        if bpth:
            if not self._bpth_called:
                self._bpth_called = True
                bpth(arg1, arg2)

    def publishTraverse(self, request, name):
        # Try to get an object using default traversal
        adapter = DefaultPublishTraverse(self.context, request)
        try:
            obj = adapter.publishTraverse(request, name)
            if not IContentish.providedBy(obj) and not IService.providedBy(obj):
                raise KeyError

        # If there's no object with the given name, we get a KeyError.
        # In a non-folderish context a key lookup results in an AttributeError.
        except (KeyError, AttributeError):
            # No object, maybe a named rest service
            service = queryMultiAdapter(
                (self.context, request), name=request._rest_service_id + name
            )
            if service is None:
                # No service, fallback to regular view
                view = queryMultiAdapter((self.context, request), name=name)
                if view is not None:
                    return view
                raise
            return service
        else:
            # Wrap object to ensure we handle further traversal
            return RESTWrapper(obj, request)

    def browserDefault(self, request):
        # Called when we have reached the end of the path
        # In our case this means an unnamed service
        return self.context, (request._rest_service_id,)

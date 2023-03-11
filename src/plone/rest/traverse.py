# -*- coding: utf-8 -*-
from plone.rest.interfaces import IAPIRequest
from plone.rest.events import mark_as_api_request
from zope.component import adapter
from zope.component import queryMultiAdapter
from zope.interface import implementer
from zope.publisher.interfaces.browser import IBrowserPublisher
from ZPublisher.BaseRequest import DefaultPublishTraverse
from zope.traversing.interfaces import ITraversable
from Products.CMFCore.interfaces import IContentish
from Products.CMFCore.interfaces import ISiteRoot


class RESTPublishTraverse(object):
    def publishTraverse(self, request, name):
        service = queryMultiAdapter(
            (self.context, request), name=request._rest_service_id + name
        )
        if service is not None:
            return service

        adapter = DefaultPublishTraverse(self.context, request)
        obj = adapter.publishTraverse(request, name)

        if IContentish.providedBy(obj) and not (
            "@@" in request["PATH_INFO"] or "++view++" in request["PATH_INFO"]
        ):
            return RESTWrapper(obj, request)

        return obj

    def browserDefault(self, request):
        # Called when we have reached the end of the path
        # In our case this means an unamed service
        return self.context, (request._rest_service_id,)


@adapter(ISiteRoot, IAPIRequest)
class RESTTraverse(RESTPublishTraverse, DefaultPublishTraverse):
    """traversal object during REST requests."""


@implementer(ITraversable)
class MarkAsRESTTraverser(object):
    """
    Traversal adapter for the ``++api++`` namespace.
    It marks the request as API request.
    """

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def traverse(self, name_ignored, subpath_ignored):
        mark_as_api_request(self.request, "application/json")
        return self.context


@implementer(IBrowserPublisher)
class RESTWrapper(RESTPublishTraverse):
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

    # MultiHook requries this to be a class attribute
    def __before_publishing_traverse__(self, arg1, arg2=None):
        bpth = getattr(self.context, "__before_publishing_traverse__", False)
        if bpth:
            if not self._bpth_called:
                self._bpth_called = True
                bpth(arg1, arg2)

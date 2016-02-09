from AccessControl import getSecurityManager
from plone.rest.interfaces import IAPIRequest
from Products.CMFCore.permissions import ManagePortal
from Products.Five.browser import BrowserView
from zExceptions import NotFound
from zope.component import adapter
from zope.component.hooks import getSite

import json
import sys
import traceback


@adapter(Exception, IAPIRequest)
class ErrorHandling(BrowserView):

    def __call__(self):
        exception = self.context
        data = self.render_exception(exception)
        result = json.dumps(data, indent=2, sort_keys=True)

        # Write and lock the response in order to avoid later changes
        # especially for Unauthorized exceptions.
        response = self.request.response
        response.setHeader('Content-Type', 'application/json')
        response.setStatus(type(exception), lock=1)
        response.setBody(result, lock=1)

        # Avoid redirect to login page on Unauthorized by adding
        # a fake challenged flag, which makes the PAS believe it
        # already did challenge and redirect.
        response._has_challenged = True
        return

    def render_exception(self, exception):
        result = {u'type': type(exception).__name__.decode('utf-8'),
                  u'message': str(exception).decode('utf-8')}

        if isinstance(exception, NotFound):
            # NotFound exceptions need special handling because their
            # exception message gets turned into HTML by ZPublisher
            url = self.request.getURL()
            result[u'message'] = u'Resource not found: %s' % url

        if getSecurityManager().checkPermission(ManagePortal, getSite()):
            result[u'traceback'] = self.render_traceback(exception)

        return result

    def render_traceback(self, exception):
        _, exc_obj, exc_traceback = sys.exc_info()
        if exception is not exc_obj:
            return (u'ERROR: Another exception happened before we could '
                    u'render the traceback.')

        raw = '\n'.join(traceback.format_tb(exc_traceback))
        return raw.strip().split('\n')

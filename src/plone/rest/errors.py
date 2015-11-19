from plone.rest.interfaces import IAPIRequest
from Products.Five.browser import BrowserView
from zope.component import adapter
import json


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
        return {u'type': type(exception).__name__.decode('utf-8'),
                u'message': str(exception).decode('utf-8')}

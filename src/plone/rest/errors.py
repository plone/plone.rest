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
        self.request.response.setHeader('Content-Type', 'application/json')
        return result

    def render_exception(self, exception):
        return {u'type': type(exception).__name__.decode('utf-8'),
                u'message': str(exception).decode('utf-8')}

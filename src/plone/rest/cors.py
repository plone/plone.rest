# -*- coding: utf-8 -*-
from plone.rest.interfaces import ICORSPolicy
from zope.interface import implements

# CORS preflight service registry
# A mapping of method -> service_id
_services = {}


def register_method_for_preflight(method, service_id):
    """Register the given method for preflighting with the given service_id."""
    _services[method] = service_id


def lookup_preflight_service_id(method):
    """Lookup a service id for the given preflighted method."""
    if method in _services:
        return _services[method]


class CORSPolicy(object):
    implements(ICORSPolicy)

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def process_simple_request(self):
        """Process the current request as a simple CORS request by setting the
           appropriate access control headers. Returns True if access control
           headers were set.
        """
        origin = self._allowed_origin()
        if not origin:
            return False

        self._process_origin_and_credentials(origin)

        if self.expose_headers:
            self.request.response.setHeader('Access-Control-Expose-Headers',
                                            ', '.join(self.expose_headers))
        return True

    def process_preflight_request(self):
        """Process the current request as a CORS preflight request by setting
           the appropriate access control headers. Returns True if access
           control headers were set.
        """
        response = self.request.response
        origin = self._allowed_origin()
        if not origin:
            return False

        method = self.request.getHeader('Access-Control-Request-Method')
        if self.allow_methods and method not in self.allow_methods:
            return False

        headers = self.request.getHeader('Access-Control-Request-Headers', '')

        # self.allow_headers is non-empty if we need to check the headers.
        if self.allow_headers:
            allowed_headers = [h.lower() for h in self.allow_headers]
            for header in headers.split(','):
                header = header.strip().lower()
                if header and header not in allowed_headers:
                    return False

        self._process_origin_and_credentials(origin)

        if self.max_age:
            response.setHeader('Access-Control-Max-Age', self.max_age)

        response.setHeader('Access-Control-Allow-Methods', method)

        if self.allow_headers:
            response.setHeader(
                'Access-Control-Allow-Headers',
                ', '.join(self.allow_headers)
            )
        elif headers:
            # allow_headers was left empty, so we will allow all headers. We
            # need to pass back the headers the client sent us, so the client
            # does not cancel the request.
            # Note: omitting Access-Control-Allow-Headers in the response is
            # allowed per specification, but not wildly supported.
            headers = self.request.getHeader(
                'Access-Control-Request-Headers', ''
            )
            self.request.response.setHeader(
                'Access-Control-Allow-Headers', headers
            )

        self.request.response.setHeader('Content-Length', '0')
        self.request.response.setStatus(200)
        return True

    def _allowed_origin(self):
        origin = self.request.getHeader('Origin', None)
        if not origin:
            return False
        if origin not in self.allow_origin and self.allow_origin != ['*']:
            return False
        return origin

    def _process_origin_and_credentials(self, origin):
        if self.allow_credentials:
            self.request.response.setHeader('Access-Control-Allow-Origin',
                                            origin)
            self.request.response.setHeader('Access-Control-Allow-Credentials',
                                            'true')
            if len(self.allow_origin) > 1 or self.allow_origin == ['*']:
                self.request.response.setHeader('Vary', 'Origin')
        elif self.allow_origin == ['*']:
            self.request.response.setHeader('Access-Control-Allow-Origin', '*')
        else:
            self.request.response.setHeader('Access-Control-Allow-Origin',
                                            origin)
            if len(self.allow_origin) > 1:
                self.request.response.setHeader('Vary', 'Origin')

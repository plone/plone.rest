# -*- coding: utf-8 -*-
from plone.rest.interfaces import IAPIRequest
from plone.rest.negotiation import lookup_service_id
from zope.interface import alsoProvides


def mark_as_api_request(event):
    """Mark a request as IAPIRequest if there's a service registered for the
       actual request method and Accept header.
    """
    request = event.request
    method = request.get('REQUEST_METHOD', 'GET')
    accept = request.getHeader('Accept', 'text/html')
    service_id = lookup_service_id(method, accept)

    if service_id is not None:
        alsoProvides(request, IAPIRequest)
        request._rest_service_id = service_id

        # Flag as non-WebDAV request in order to avoid special treatment
        # in ZPublisher.BaseRequest.traverse().
        request.maybe_webdav_client = 0

# -*- coding: utf-8 -*-
from plone.rest.interfaces import IAPIRequest
from plone.rest.interfaces import IPUT
from plone.rest.interfaces import IGET
from plone.rest.interfaces import IPOST
from plone.rest.interfaces import IDELETE
from plone.rest.interfaces import IOPTIONS
from plone.rest.interfaces import IPATCH
from zope.interface import alsoProvides


def mark_as_api_request(event):
    """Mark a request with Accept 'application/json' with the IAPIRequest
       interface.
    """
    # In cors calls there is accept header so we need to force
    method = event.request.get('REQUEST_METHOD')
    if method == 'OPTIONS' and event.request.getHeader('Origin', None):
        alsoProvides(event.request, IAPIRequest)
        alsoProvides(event.request, IOPTIONS)
        # May have problems with webdav
        # All OPTIONS calls are going to be considered API/REST
        event.request.maybe_webdav_client = 0
    request = event.request
    if request.getHeader('Accept') == 'application/json':
        alsoProvides(request, IAPIRequest)
        if method == 'PUT':
            alsoProvides(request, IPUT)
        if method == 'DELETE':
            alsoProvides(request, IDELETE)
        if method == 'GET':
            alsoProvides(request, IGET)
        if method == 'POST':
            alsoProvides(request, IPOST)
        if method == 'OPTIONS':
            alsoProvides(request, IOPTIONS)
        if method == 'PATCH':
            alsoProvides(request, IPATCH)

        # Flag as non-WebDAV request in order to avoid special treatment
        # in ZPublisher.BaseRequest.traverse().
        event.request.maybe_webdav_client = 0

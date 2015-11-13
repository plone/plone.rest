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
    request = event.request
    if request.getHeader('Accept') == 'application/json':
        alsoProvides(request, IAPIRequest)
        if request.get('REQUEST_METHOD') == 'PUT':
            alsoProvides(request, IPUT)
        if request.get('REQUEST_METHOD') == 'DELETE':
            alsoProvides(request, IDELETE)
        if request.get('REQUEST_METHOD') == 'GET':
            alsoProvides(request, IGET)
        if request.get('REQUEST_METHOD') == 'POST':
            alsoProvides(request, IPOST)
        if request.get('REQUEST_METHOD') == 'OPTIONS':
            alsoProvides(request, IOPTIONS)
        if request.get('REQUEST_METHOD') == 'PATCH':
            alsoProvides(request, IPATCH)

        # Flag as non-WebDAV request in order to avoid special treatment
        # in ZPublisher.BaseRequest.traverse().
        event.request.maybe_webdav_client = 0

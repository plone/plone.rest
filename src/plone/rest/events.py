# -*- coding: utf-8 -*-
from plone.rest.interfaces import IAPIRequest
from plone.rest.interfaces import IPUT
from plone.rest.interfaces import IGET
from plone.rest.interfaces import IPOST
from plone.rest.interfaces import IDELETE
from plone.rest.interfaces import IOPTIONS
from plone.rest.interfaces import IPATCH
from zope.interface import alsoProvides


def mark_as_api_request(context, event):
    """Mark a request with Accept 'application/json' with the IAPIRequest
       interface.
    """
    if event.request.getHeader('Accept') == 'application/json':
        alsoProvides(event.request, IAPIRequest)
        if event.request.get('REQUEST_METHOD') == 'PUT':
            alsoProvides(event.request, IPUT)
        if event.request.get('REQUEST_METHOD') == 'DELETE':
            alsoProvides(event.request, IDELETE)
        if event.request.get('REQUEST_METHOD') == 'GET':
            alsoProvides(event.request, IGET)
        if event.request.get('REQUEST_METHOD') == 'POST':
            alsoProvides(event.request, IPOST)
        if event.request.get('REQUEST_METHOD') == 'OPTIONS':
            alsoProvides(event.request, IOPTIONS)
        if event.request.get('REQUEST_METHOD') == 'PATCH':
            alsoProvides(event.request, IPATCH)

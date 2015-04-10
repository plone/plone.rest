from plone.rest.interfaces import IAPIRequest
from zope.interface import alsoProvides
from plone.rest.interfaces import IPUT, IGET, IPOST, IDELETE, IOPTIONS, IPATCH


def mark_as_api_request(context, event):
    """Mark views with application/json as Content-Type with the IAPIRequest
       interface.
    """
    if event.request.getHeader('Content-Type') == 'application/json':
        alsoProvides(event.request, IAPIRequest)  # pragma: no cover
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

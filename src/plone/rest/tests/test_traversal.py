# -*- coding: utf-8 -*-
from ZPublisher.pubevents import PubStart
from base64 import b64encode
from plone.app.testing import SITE_OWNER_NAME
from plone.app.testing import SITE_OWNER_PASSWORD
from plone.rest.service import Service
from plone.rest.testing import PLONE_REST_INTEGRATION_TESTING
from zope.event import notify

import unittest


class TestTraversal(unittest.TestCase):

    layer = PLONE_REST_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']

    def traverse(self, path='/plone', accept='application/json', method='GET'):
        request = self.layer['request']
        request.environ['PATH_INFO'] = path
        request.environ['PATH_TRANSLATED'] = path
        request.environ['HTTP_ACCEPT'] = accept
        request.environ['REQUEST_METHOD'] = method
        request._auth = 'Basic %s' % b64encode(
            '%s:%s' % (SITE_OWNER_NAME, SITE_OWNER_PASSWORD))
        notify(PubStart(request))
        return request.traverse(path)

    def test_json_request_on_portal_root_returns_service(self):
        obj = self.traverse()
        self.assertTrue(isinstance(obj, Service), 'Not a service')

    def test_json_request_on_portal_root_with_layout_returns_service(self):
        self.portal.setLayout('summary_view')
        obj = self.traverse()
        self.assertTrue(isinstance(obj, Service), 'Not a service')

    def test_json_request_on_portal_root_with_default_page_returns_service(
            self):
        self.portal.invokeFactory('Document', id='doc1')
        self.portal.setDefaultPage('doc1')
        obj = self.traverse()
        self.assertTrue(isinstance(obj, Service), 'Not a service')

    def test_json_request_on_content_object_returns_service(self):
        self.portal.invokeFactory('Document', id='doc1')
        obj = self.traverse(path='/plone/doc1')
        self.assertTrue(isinstance(obj, Service), 'Not a service')

    def test_html_request_on_portal_root_returns_default_view(self):
        obj = self.traverse(accept='text/html')
        self.assertEquals('listing_view', obj.__name__)

    def test_html_request_on_portal_root_returns_dynamic_view(self):
        self.portal.setLayout('summary_view')
        obj = self.traverse(accept='text/html')
        self.assertEquals('summary_view', obj.__name__)

    def test_html_request_on_portal_root_returns_default_page(self):
        self.portal.invokeFactory('Document', id='doc1')
        self.portal.setDefaultPage('doc1')
        obj = self.traverse(accept='text/html')
        self.assertEquals('document_view', obj.__name__)

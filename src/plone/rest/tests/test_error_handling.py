# -*- coding: utf-8 -*-
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing import SITE_OWNER_NAME
from plone.app.testing import SITE_OWNER_PASSWORD
from plone.rest.testing import PLONE_REST_FUNCTIONAL_TESTING
from Products.Five.browser import BrowserView
from zope.component import provideAdapter
from zope.interface import Interface
from zope.publisher.interfaces.browser import IBrowserRequest

import json
import requests
import transaction
import unittest


class InternalServerErrorView(BrowserView):

    def __call__(self):  # pragma: no cover
        from urllib2 import HTTPError
        raise HTTPError(
            'http://nohost/plone/internal_server_error',
            500,
            'InternalServerError',
            {},
            None
        )
        raise HTTPError


class TestErrorHandling(unittest.TestCase):

    layer = PLONE_REST_FUNCTIONAL_TESTING

    def setUp(self):
        self.app = self.layer['app']
        self.request = self.layer['request']
        self.portal = self.layer['portal']
        self.portal_url = self.portal.absolute_url()
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory('Document', id='document1')
        self.document = self.portal.document1
        self.document_url = self.document.absolute_url()
        self.portal.invokeFactory('Folder', id='folder1')
        self.folder = self.portal.folder1
        self.folder_url = self.folder.absolute_url()
        transaction.commit()

    def test_404_not_found(self):
        response = requests.get(
            self.portal_url + '/non-existing-resource',
            headers={'Accept': 'application/json'},
            auth=(SITE_OWNER_NAME, SITE_OWNER_PASSWORD)
        )
        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response.headers.get('Content-Type'),
            'application/json',
            'When sending a GET request with Accept: application/json ' +
            'the server should respond with sending back application/json.'
        )
        self.assertTrue(json.loads(response.content))
        self.assertEqual(
            'NotFound',
            response.json()['type']
        )

    def test_401_unauthorized(self):
        response = requests.get(
            self.document_url,
            headers={'Accept': 'application/json'}
        )
        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            response.headers.get('Content-Type'),
            'application/json',
            'When sending a GET request with Accept: application/json ' +
            'the server should respond with sending back application/json.'
        )
        self.assertNotIn('Location', response.headers,
                         'A 401 unauthorized should not redirect.')
        self.assertTrue(json.loads(response.content))
        self.assertEqual(
            'Unauthorized',
            response.json()['type']
        )

    def test_500_internal_server_error(self):
        provideAdapter(
            InternalServerErrorView,
            adapts=(Interface, IBrowserRequest),
            provides=Interface,
            name='internal_server_error'
        )
        import transaction
        transaction.commit()

        response = requests.get(
            self.portal_url + '/internal_server_error',
            headers={'Accept': 'application/json'}
        )

        self.assertEqual(response.status_code, 500)
        self.assertEqual(
            response.headers.get('Content-Type'),
            'application/json',
            'When sending a GET request with Accept: application/json ' +
            'the server should respond with sending back application/json.'
        )
        self.assertTrue(json.loads(response.content))
        self.assertEqual(
            'HTTPError',
            response.json()['type']
        )

        self.assertEqual(
            {u'type': u'HTTPError',
             u'message': u'HTTP Error 500: InternalServerError'},
            response.json())

# -*- coding: utf-8 -*-
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_PASSWORD
from plone.app.testing import SITE_OWNER_NAME
from plone.app.testing import SITE_OWNER_PASSWORD
from plone.rest.testing import PLONE_REST_FUNCTIONAL_TESTING

import json
import requests
import transaction
import unittest


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
        self.assertEqual(
            'Resource not found: %s' % response.url,
            response.json()['message']
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
        response = requests.get(
            self.portal_url + '/500-internal-server-error',
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

    def test_500_traceback_only_for_manager_users(self):
        # Normal user
        response = requests.get(
            self.portal_url + '/500-internal-server-error',
            headers={'Accept': 'application/json'},
            auth=(TEST_USER_ID, TEST_USER_PASSWORD)
        )
        self.assertNotIn(u'traceback', response.json())

        # Manager user
        response = requests.get(
            self.portal_url + '/500-internal-server-error',
            headers={'Accept': 'application/json'},
            auth=(SITE_OWNER_NAME, SITE_OWNER_PASSWORD)
        )
        self.assertIn(u'traceback', response.json())

        traceback = response.json()[u'traceback']
        self.assertIsInstance(traceback, list)
        self.assertRegexpMatches(
            traceback[0],
            r'^File "[^"]*", line \d*, in (publish|transaction_pubevents)')

    def test_api_exception(self):
        response = requests.get(
            self.portal_url + '/api-exception?status=400&details=dict',
            headers={'Accept': 'application/json'},
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.headers.get('Content-Type'),
            'application/json',
            'When sending a GET request with Accept: application/json ' +
            'the server should respond with sending back application/json.'
        )
        response = response.json()
        self.assertEqual(
            response,
            {
                'type': 'error400',
                'message': 'errormessage for error 400',
                'details': {
                    'foo': 'bar',
                }
            }
        )

    def test_api_exception_with_dict_details(self):
        response = requests.get(
            self.portal_url + '/api-exception?status=400&details=dict',
            headers={'Accept': 'application/json'},
        )

        self.assertEqual(response.json()['details'], {'foo': 'bar'})

    def test_api_exception_with_list_details(self):
        response = requests.get(
            self.portal_url + '/api-exception?status=400&details=list',
            headers={'Accept': 'application/json'},
        )

        self.assertEqual(response.json()['details'], ['foo', 'bar'])

    def test_api_exception_with_string_details(self):
        response = requests.get(
            self.portal_url + '/api-exception?status=400&details=string',
            headers={'Accept': 'application/json'},
        )

        self.assertEqual(response.json()['details'], 'foobar')

    def test_api_exception_without_details(self):
        response = requests.get(
            self.portal_url + '/api-exception?status=400&details=none',
            headers={'Accept': 'application/json'},
        )

        self.assertEqual(response.json()['details'], None)

    def test_api_exception_with_traceback(self):
        self.maxDiff = None
        response = requests.get(
            self.portal_url + '/api-exception-with-traceback',
            headers={'Accept': 'application/json'},
        )
        response = response.json()

        self.assertEqual(
            sorted(response['details'].keys()),
            ['Just kidding', 'traceback'])
        self.assertTrue(
            "raise AssertionError('You should not call this method')" in
            ' '.join(response['details']['traceback']))

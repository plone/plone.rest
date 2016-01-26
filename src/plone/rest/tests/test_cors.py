# -*- coding: utf-8 -*-
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing import SITE_OWNER_NAME
from plone.app.testing import SITE_OWNER_PASSWORD
from plone.rest.testing import PLONE_REST_FUNCTIONAL_TESTING

import unittest
import requests
import transaction


class TestDexterityServiceEndpoints(unittest.TestCase):

    layer = PLONE_REST_FUNCTIONAL_TESTING

    def setUp(self):
        self.app = self.layer['app']
        self.request = self.layer['request']
        self.portal = self.layer['portal']
        self.portal_url = self.portal.absolute_url()
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory('Document', id='doc1')
        self.document = self.portal['doc1']
        transaction.commit()

    def test_preflight_cors_dexterity(self):

        response = requests.options(
            self.document.absolute_url(),
            headers={
                'Accept': '*/*',
                'Origin': 'plone.org',
                'Access-Control-Request-Method': 'POST'},
            auth=(SITE_OWNER_NAME, SITE_OWNER_PASSWORD)
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue('Access-Control-Allow-Methods' in response.headers)
        self.assertEqual(
            'GET,PATCH,PUT,POST,OPTIONS,DELETE',
            response.headers['Access-Control-Allow-Methods']
        )

        response = requests.post(
            self.document.absolute_url(),
            headers={
                'Accept': 'application/json',
                'Origin': 'plone.org'},
            auth=(SITE_OWNER_NAME, SITE_OWNER_PASSWORD)
        )

        self.assertEqual(response.status_code, 200)

    def test_cors_dexterity_origin(self):

        response = requests.options(
            self.document.absolute_url() + '/corsexample',
            headers={
                'Accept': 'application/json',
                'Origin': 'foobar',
                'Access-Control-Request-Method': 'POST',
                'Access-Control-Request-Headers': 'accept, content-type'},
            auth=(SITE_OWNER_NAME, SITE_OWNER_PASSWORD)
        )

        self.assertEqual(response.status_code, 200)

        self.assertEqual(
            'POST,GET',
            response.headers['Access-Control-Allow-Methods']
        )
        self.assertEqual(
            'foobar',
            response.headers['Access-Control-Allow-Origin']
        )

        response = requests.post(
            self.document.absolute_url(),
            headers={
                'Accept': 'application/json',
                'Origin': 'foobar'},
            auth=(SITE_OWNER_NAME, SITE_OWNER_PASSWORD)
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            '*',
            response.headers['Access-Control-Allow-Origin']
        )

    def test_cors_no_headers(self):

        response = requests.options(
            self.document.absolute_url() + '/corsexample',
            headers={'Accept': 'application/json'},
            auth=(SITE_OWNER_NAME, SITE_OWNER_PASSWORD)
        )

        self.assertEqual(response.status_code, 404)

    def test_cors_dexterity_bad_origin(self):

        response = requests.options(
            self.document.absolute_url() + '/corsexample',
            headers={
                'Accept': 'application/json',
                'Origin': 'plone.org',
                'Access-Control-Request-Method': 'POST',
                'Access-Control-Request-Headers': 'accept, content-type'},
            auth=(SITE_OWNER_NAME, SITE_OWNER_PASSWORD)
        )

        self.assertEqual(response.status_code, 404)

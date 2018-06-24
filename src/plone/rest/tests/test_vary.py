# -*- coding: utf-8 -*-
from plone.rest.testing import PLONE_REST_FUNCTIONAL_TESTING
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing import SITE_OWNER_NAME
from plone.app.testing import SITE_OWNER_PASSWORD

import unittest
import requests


class TestEndpointsAddVaryHeader(unittest.TestCase):

    layer = PLONE_REST_FUNCTIONAL_TESTING

    def setUp(self):
        self.app = self.layer['app']
        self.request = self.layer['request']
        self.portal = self.layer['portal']
        self.portal_url = self.portal.absolute_url()
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

    def test_non_api_query_has_vary_header(self):
        response = requests.get(
            self.portal.absolute_url(),
            auth=(SITE_OWNER_NAME, SITE_OWNER_PASSWORD)
        )
        self.assertIn('Vary', response.headers)
        self.assertEqual('Accept', response.headers.get('Vary'))

    def test_api_request_has_vary_header(self):
        response = requests.get(
            self.portal.absolute_url(),
            headers={'Accept': 'application/json'},
            auth=(SITE_OWNER_NAME, SITE_OWNER_PASSWORD)
        )
        self.assertIn('Vary', response.headers)
        self.assertEqual('Accept', response.headers.get('Vary'))

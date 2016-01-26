# -*- coding: utf-8 -*-
from plone.rest.testing import PLONE_REST_FUNCTIONAL_TESTING
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing import SITE_OWNER_NAME
from plone.app.testing import SITE_OWNER_PASSWORD

import unittest
import requests


class TestSiteRootServiceEndpoints(unittest.TestCase):

    layer = PLONE_REST_FUNCTIONAL_TESTING

    def setUp(self):
        self.app = self.layer['app']
        self.request = self.layer['request']
        self.portal = self.layer['portal']
        self.portal_url = self.portal.absolute_url()
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

    def test_siteroot_get(self):
        response = requests.get(
            self.portal.absolute_url(),
            headers={'Accept': 'application/json'},
            auth=(SITE_OWNER_NAME, SITE_OWNER_PASSWORD)
        )
        self.assertEqual(
            response.status_code,
            200,
            'GET /Plone should return status code 200, not {}'.format(
                response.status_code
            )
        )
        self.assertEqual(
            {u'portal_id': u'plone'},
            response.json()
        )

    def test_siteroot_post(self):
        response = requests.post(
            self.portal.absolute_url(),
            headers={'Accept': 'application/json'},
            auth=(SITE_OWNER_NAME, SITE_OWNER_PASSWORD)
        )
        self.assertEqual(
            response.status_code,
            200,
            'POST /Plone should return status code 201, not {}'.format(
                response.status_code
            )
        )
        self.assertTrue(response.json())
        self.assertEqual(
            {u'service': u'post'},
            response.json()
        )

    def test_siteroot_delete(self):
        response = requests.delete(
            self.portal.absolute_url(),
            headers={'Accept': 'application/json'},
            auth=(SITE_OWNER_NAME, SITE_OWNER_PASSWORD)
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            {u'service': u'delete'},
            response.json()
        )

    def test_siteroot_put(self):
        response = requests.put(
            self.portal.absolute_url(),
            headers={'Accept': 'application/json'},
            auth=(SITE_OWNER_NAME, SITE_OWNER_PASSWORD)
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            {u'service': u'put'},
            response.json()
        )

    def test_siteroot_patch(self):
        response = requests.patch(
            self.portal.absolute_url(),
            headers={'Accept': 'application/json'},
            auth=(SITE_OWNER_NAME, SITE_OWNER_PASSWORD)
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            {u'service': u'patch'},
            response.json()
        )

    def test_siteroot_options(self):
        response = requests.options(
            self.portal.absolute_url(),
            headers={
                'Accept': 'application/json',
                'Access-Control-Request-Method': 'OPTIONS',
                'Origin': 'foobar'},
            auth=(SITE_OWNER_NAME, SITE_OWNER_PASSWORD)
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            {u'service': u'options'},
            response.json()
        )

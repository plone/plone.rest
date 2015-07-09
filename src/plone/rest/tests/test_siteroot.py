# -*- coding: utf-8 -*-
from plone.rest.testing import PLONE_REST_FUNCTIONAL_TESTING
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing import SITE_OWNER_NAME
from plone.app.testing import SITE_OWNER_PASSWORD
from plone.testing.z2 import Browser

import unittest2 as unittest

import json
import requests


class TestSiteRoot(unittest.TestCase):

    layer = PLONE_REST_FUNCTIONAL_TESTING

    def setUp(self):
        self.app = self.layer['app']
        self.request = self.layer['request']
        self.portal = self.layer['portal']
        self.portal_url = self.portal.absolute_url()
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.browser = Browser(self.app)
        self.browser.handleErrors = False
        self.browser.addHeader(
            'Authorization',
            'Basic %s:%s' % (SITE_OWNER_NAME, SITE_OWNER_PASSWORD,)
        )

    def test_siteroot_get(self):
        response = requests.get(
            self.portal.absolute_url(),
            headers={'content-type': 'application/json'},
            auth=(SITE_OWNER_NAME, SITE_OWNER_PASSWORD)
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(json.loads(response.text))

    def test_siteroot_post(self):
        response = requests.post(
            self.portal.absolute_url(),
            headers={'content-type': 'application/json'},
            auth=(SITE_OWNER_NAME, SITE_OWNER_PASSWORD)
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(json.loads(response.text))

    def test_siteroot_delete(self):
        response = requests.delete(
            self.portal.absolute_url(),
            headers={'content-type': 'application/json'},
            auth=(SITE_OWNER_NAME, SITE_OWNER_PASSWORD)
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(json.loads(response.text))

    def test_siteroot_put(self):
        response = requests.put(
            self.portal.absolute_url(),
            headers={'content-type': 'application/json'},
            auth=(SITE_OWNER_NAME, SITE_OWNER_PASSWORD)
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(json.loads(response.text))

    def test_siteroot_patch(self):
        response = requests.patch(
            self.portal.absolute_url(),
            headers={'content-type': 'application/json'},
            auth=(SITE_OWNER_NAME, SITE_OWNER_PASSWORD)
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(json.loads(response.text))

    def test_siteroot_options(self):
        response = requests.options(
            self.portal.absolute_url(),
            headers={'content-type': 'application/json'},
            auth=(SITE_OWNER_NAME, SITE_OWNER_PASSWORD)
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(json.loads(response.text))

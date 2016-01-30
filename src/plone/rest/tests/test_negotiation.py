# -*- coding: utf-8 -*-
from plone.rest.testing import PLONE_REST_FUNCTIONAL_TESTING
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing import SITE_OWNER_NAME
from plone.app.testing import SITE_OWNER_PASSWORD

import transaction
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
        self.portal.invokeFactory('Document', id='doc1')
        self.document = self.portal['doc1']

        transaction.commit()

    def test_negotiation_wildcard(self):
        response = requests.patch(
            self.document.absolute_url() + '/negotiation_wildcard',
            headers={'Accept': 'myown/content'},
            auth=(SITE_OWNER_NAME, SITE_OWNER_PASSWORD)
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            {u'service': u'named get'},
            response.json()
        )

    def test_negotiation_one_wildcard(self):
        response = requests.head(
            self.document.absolute_url() + '/negotiation_one_wildcard',
            headers={'Accept': 'application/json'},
            auth=(SITE_OWNER_NAME, SITE_OWNER_PASSWORD)
        )
        self.assertEqual(response.status_code, 404)

        response = requests.head(
            self.document.absolute_url() + '/negotiation_one_wildcard',
            headers={'Accept': 'image/json'},
            auth=(SITE_OWNER_NAME, SITE_OWNER_PASSWORD)
        )

        self.assertEqual(response.status_code, 200)

    def test_negotiation_no_wildcard(self):
        response = requests.put(
            self.document.absolute_url() + '/negotiation_no_wildcard',
            headers={'Accept': 'application/json'},
            auth=(SITE_OWNER_NAME, SITE_OWNER_PASSWORD)
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            {u'service': u'named get'},
            response.json()
        )

        response = requests.put(
            self.document.absolute_url() + '/negotiation_no_wildcard',
            headers={'Accept': 'text/html'},
            auth=(SITE_OWNER_NAME, SITE_OWNER_PASSWORD)
        )
        self.assertEqual(response.status_code, 404)

        response = requests.put(
            self.document.absolute_url() + '/negotiation_no_wildcard',
            headers={'Accept': 'application/json'},
            auth=(SITE_OWNER_NAME, SITE_OWNER_PASSWORD)
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            {u'service': u'named get'},
            response.json()
        )

        response = requests.put(
            self.document.absolute_url() + '/negotiation_no_wildcard',
            headers={'Accept': 'text/xhtml'},
            auth=(SITE_OWNER_NAME, SITE_OWNER_PASSWORD)
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            {u'service': u'named get'},
            response.json()
        )

        response = requests.put(
            self.document.absolute_url() + '/negotiation_no_wildcard',
            headers={'Accept': 'text/plain'},
            auth=(SITE_OWNER_NAME, SITE_OWNER_PASSWORD)
        )
        self.assertEqual(response.status_code, 404)

# -*- coding: utf-8 -*-
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing import SITE_OWNER_NAME
from plone.app.testing import SITE_OWNER_PASSWORD
from plone.rest.testing import PLONE_REST_FUNCTIONAL_TESTING

import unittest
import requests
import transaction


class TestNamedServiceEndpoints(unittest.TestCase):

    layer = PLONE_REST_FUNCTIONAL_TESTING

    def setUp(self):
        self.app = self.layer["app"]
        self.request = self.layer["request"]
        self.portal = self.layer["portal"]
        self.portal_url = self.portal.absolute_url()
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self.portal.invokeFactory("Document", id="doc1")
        self.document = self.portal["doc1"]
        transaction.commit()

    def test_dexterity_named_get(self):
        response = requests.get(
            self.document.absolute_url() + "/namedservice",
            headers={"Accept": "application/json"},
            auth=(SITE_OWNER_NAME, SITE_OWNER_PASSWORD),
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual({u"service": u"named get"}, response.json())

    def test_dexterity_named_post(self):
        response = requests.post(
            self.document.absolute_url() + "/namedservice",
            headers={"Accept": "application/json"},
            auth=(SITE_OWNER_NAME, SITE_OWNER_PASSWORD),
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual({u"service": u"named post"}, response.json())

    def test_dexterity_named_put(self):
        response = requests.put(
            self.document.absolute_url() + "/namedservice",
            headers={"Accept": "application/json"},
            auth=(SITE_OWNER_NAME, SITE_OWNER_PASSWORD),
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual({u"service": u"named put"}, response.json())

    def test_dexterity_named_patch(self):
        response = requests.patch(
            self.document.absolute_url() + "/namedservice",
            headers={"Accept": "application/json"},
            auth=(SITE_OWNER_NAME, SITE_OWNER_PASSWORD),
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual({u"service": u"named patch"}, response.json())

    def test_dexterity_named_delete(self):
        response = requests.delete(
            self.document.absolute_url() + "/namedservice",
            headers={"Accept": "application/json"},
            auth=(SITE_OWNER_NAME, SITE_OWNER_PASSWORD),
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual({u"service": u"named delete"}, response.json())

    def test_dexterity_named_options(self):
        response = requests.options(
            self.document.absolute_url() + "/namedservice",
            headers={"Accept": "application/json"},
            auth=(SITE_OWNER_NAME, SITE_OWNER_PASSWORD),
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual({u"service": u"named options"}, response.json())

from plone.app.testing import setRoles
from plone.app.testing import SITE_OWNER_NAME
from plone.app.testing import SITE_OWNER_PASSWORD
from plone.app.testing import TEST_USER_ID
from plone.rest.testing import PLONE_REST_FUNCTIONAL_TESTING

import requests
import unittest


class TestSiteRootServiceEndpoints(unittest.TestCase):
    layer = PLONE_REST_FUNCTIONAL_TESTING

    def setUp(self):
        self.app = self.layer["app"]
        self.request = self.layer["request"]
        self.portal = self.layer["portal"]
        self.portal_url = self.portal.absolute_url()
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

    def test_siteroot_get(self):
        response = requests.get(
            self.portal.absolute_url(),
            headers={"Accept": "application/json"},
            auth=(SITE_OWNER_NAME, SITE_OWNER_PASSWORD),
        )
        self.assertEqual(
            response.status_code,
            200,
            "GET /Plone should return status code 200, not {}".format(
                response.status_code
            ),
        )
        self.assertEqual("plone", response.json().get("id"))
        self.assertEqual("GET", response.json().get("method"))

    def test_siteroot_post(self):
        response = requests.post(
            self.portal.absolute_url(),
            headers={"Accept": "application/json"},
            auth=(SITE_OWNER_NAME, SITE_OWNER_PASSWORD),
        )
        self.assertEqual(
            response.status_code,
            200,
            "POST /Plone should return status code 201, not {}".format(
                response.status_code
            ),
        )
        self.assertEqual("plone", response.json().get("id"))
        self.assertEqual("POST", response.json().get("method"))

    def test_siteroot_delete(self):
        response = requests.delete(
            self.portal.absolute_url(),
            headers={"Accept": "application/json"},
            auth=(SITE_OWNER_NAME, SITE_OWNER_PASSWORD),
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual("plone", response.json().get("id"))
        self.assertEqual("DELETE", response.json().get("method"))

    def test_siteroot_put(self):
        response = requests.put(
            self.portal.absolute_url(),
            headers={"Accept": "application/json"},
            auth=(SITE_OWNER_NAME, SITE_OWNER_PASSWORD),
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual("plone", response.json().get("id"))
        self.assertEqual("PUT", response.json().get("method"))

    def test_siteroot_patch(self):
        response = requests.patch(
            self.portal.absolute_url(),
            headers={"Accept": "application/json"},
            auth=(SITE_OWNER_NAME, SITE_OWNER_PASSWORD),
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual("plone", response.json().get("id"))
        self.assertEqual("PATCH", response.json().get("method"))

    def test_siteroot_options(self):
        response = requests.options(
            self.portal.absolute_url(),
            headers={"Accept": "application/json"},
            auth=(SITE_OWNER_NAME, SITE_OWNER_PASSWORD),
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual("plone", response.json().get("id"))
        self.assertEqual("OPTIONS", response.json().get("method"))

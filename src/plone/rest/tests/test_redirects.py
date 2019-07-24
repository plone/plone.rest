# -*- coding: utf-8 -*-
from BTrees.OOBTree import OOSet
from plone.app.redirector.interfaces import IRedirectionStorage
from plone.app.testing import setRoles
from plone.app.testing import SITE_OWNER_NAME
from plone.app.testing import SITE_OWNER_PASSWORD
from plone.app.testing import TEST_USER_ID
from plone.rest.errors import ErrorHandling
from plone.rest.testing import PLONE_REST_FUNCTIONAL_TESTING
from zope.component import queryUtility

import requests
import transaction
import unittest


class TestRedirects(unittest.TestCase):

    layer = PLONE_REST_FUNCTIONAL_TESTING

    def setUp(self):
        self.app = self.layer["app"]
        self.portal = self.layer["portal"]
        self.portal_url = self.portal.absolute_url()
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

        self.portal.invokeFactory("Folder", id="folder-old")
        self.portal.manage_renameObject("folder-old", "folder-new")
        transaction.commit()

    def test_get_to_moved_item_causes_301_redirect(self):
        response = requests.get(
            self.portal_url + "/folder-old",
            headers={"Accept": "application/json"},
            auth=(SITE_OWNER_NAME, SITE_OWNER_PASSWORD),
            allow_redirects=False,
        )
        self.assertEqual(301, response.status_code)
        self.assertEqual(self.portal_url + "/folder-new", response.headers["Location"])
        self.assertEqual(b"", response.raw.read())

    def test_post_to_moved_item_causes_308_redirect(self):
        response = requests.post(
            self.portal_url + "/folder-old",
            headers={"Accept": "application/json"},
            auth=(SITE_OWNER_NAME, SITE_OWNER_PASSWORD),
            allow_redirects=False,
        )
        self.assertEqual(308, response.status_code)
        self.assertEqual(self.portal_url + "/folder-new", response.headers["Location"])
        self.assertEqual(b"", response.raw.read())

    def test_unauthorized_request_to_item_still_redirects_first(self):
        response = requests.get(
            self.portal_url + "/folder-old",
            headers={"Accept": "application/json"},
            # No auth
            allow_redirects=False,
        )

        # A request to the old URL of an item where the user doesn't have
        # necessary permissions will still result in a redirect
        self.assertEqual(301, response.status_code)
        self.assertEqual(self.portal_url + "/folder-new", response.headers["Location"])
        self.assertEqual(b"", response.raw.read())

        # Following the redirect then leads to an item that will produce a 401
        response = requests.get(
            response.headers["Location"],
            headers={"Accept": "application/json"},
            # No auth
            allow_redirects=False,
        )
        self.assertEqual(401, response.status_code)

    def test_query_string_gets_preserved(self):
        response = requests.get(
            self.portal_url + "/folder-old?key=value",
            headers={"Accept": "application/json"},
            auth=(SITE_OWNER_NAME, SITE_OWNER_PASSWORD),
            allow_redirects=False,
        )
        self.assertEqual(301, response.status_code)
        self.assertEqual(
            self.portal_url + "/folder-new?key=value", response.headers["Location"]
        )
        self.assertEqual(b"", response.raw.read())

    def test_named_service_on_moved_item_causes_301_redirect(self):
        response = requests.get(
            self.portal_url + "/folder-old/namedservice",
            headers={"Accept": "application/json"},
            auth=(SITE_OWNER_NAME, SITE_OWNER_PASSWORD),
            allow_redirects=False,
        )
        self.assertEqual(301, response.status_code)
        self.assertEqual(
            self.portal_url + "/folder-new/namedservice", response.headers["Location"]
        )
        self.assertEqual(b"", response.raw.read())

    def test_named_service_plus_path_parameter_works(self):
        response = requests.get(
            self.portal_url + "/folder-old/namedservice/param",
            headers={"Accept": "application/json"},
            auth=(SITE_OWNER_NAME, SITE_OWNER_PASSWORD),
            allow_redirects=False,
        )
        self.assertEqual(301, response.status_code)
        self.assertEqual(
            self.portal_url + "/folder-new/namedservice/param",
            response.headers["Location"],
        )
        self.assertEqual(b"", response.raw.read())

    def test_redirects_for_regular_views_still_work(self):
        response = requests.get(
            self.portal_url + "/folder-old/@@some-view",
            headers={"Accept": "application/json"},
            auth=(SITE_OWNER_NAME, SITE_OWNER_PASSWORD),
            allow_redirects=False,
        )
        self.assertEqual(301, response.status_code)
        self.assertEqual(
            self.portal_url + "/folder-new/@@some-view", response.headers["Location"]
        )
        self.assertEqual(b"", response.raw.read())

    def test_redirects_for_views_plus_params_plus_querystring_works(self):
        response = requests.get(
            self.portal_url + "/folder-old/@@some-view/param?k=v",
            headers={"Accept": "application/json"},
            auth=(SITE_OWNER_NAME, SITE_OWNER_PASSWORD),
            allow_redirects=False,
        )
        self.assertEqual(301, response.status_code)
        self.assertEqual(
            self.portal_url + "/folder-new/@@some-view/param?k=v",
            response.headers["Location"],
        )
        self.assertEqual(b"", response.raw.read())

    def test_doesnt_cause_redirect_loop_on_bogus_storage_entries(self):
        storage = queryUtility(IRedirectionStorage)
        storage._paths["/plone/same"] = "/plone/same"
        storage._rpaths["/plone/same"] = OOSet(["/plone/same"])
        transaction.commit()

        response = requests.get(
            self.portal_url + "/same/@@view",
            headers={"Accept": "application/json"},
            auth=(SITE_OWNER_NAME, SITE_OWNER_PASSWORD),
            allow_redirects=False,
        )
        self.assertEqual(404, response.status_code)

    def test_handles_redirects_that_include_querystring_in_old_path(self):
        storage = queryUtility(IRedirectionStorage)
        storage.add("/plone/some-item?key=value", "/plone/new-item")
        transaction.commit()

        response = requests.get(
            self.portal_url + "/some-item?key=value",
            headers={"Accept": "application/json"},
            auth=(SITE_OWNER_NAME, SITE_OWNER_PASSWORD),
            allow_redirects=False,
        )
        self.assertEqual(301, response.status_code)
        self.assertEqual(self.portal_url + "/new-item", response.headers["Location"])
        self.assertEqual(b"", response.raw.read())

    def test_aborts_redirect_checks_early_for_app_root(self):
        error_view = ErrorHandling(self.portal, self.portal.REQUEST)
        self.assertIsNone(error_view.find_redirect_if_view_or_service([""], None))

    def test_gracefully_deals_with_missing_request_url(self):
        error_view = ErrorHandling(self.portal, self.portal.REQUEST)
        self.portal.REQUEST["ACTUAL_URL"] = None
        self.assertEquals(False, error_view.attempt_redirect())

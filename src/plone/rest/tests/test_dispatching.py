# -*- coding: utf-8 -*-
from plone.app.testing import setRoles
from plone.app.testing import SITE_OWNER_NAME
from plone.app.testing import SITE_OWNER_PASSWORD
from plone.app.testing import TEST_USER_ID
from plone.rest.testing import PLONE_REST_FUNCTIONAL_TESTING
from Products.CMFCore.utils import getToolByName

import requests
import transaction
import unittest


CREDS = (SITE_OWNER_NAME, SITE_OWNER_PASSWORD)
INVALID_CREDS = ("invalid", "password")
NO_CREDS = ()


class DispatchingTestCase(unittest.TestCase):

    layer = PLONE_REST_FUNCTIONAL_TESTING

    def setUp(self):
        self.app = self.layer["app"]
        self.request = self.layer["request"]
        self.portal = self.layer["portal"]
        self.portal_url = self.portal.absolute_url()
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

    def validate(self, expectations, follow_redirects=False):
        failures = []
        for expectation in expectations:
            path, method, creds, expected_status = expectation
            url = self.portal_url + path

            response = requests.request(
                method,
                url,
                headers={"Accept": "application/json"},
                auth=creds,
                allow_redirects=follow_redirects,
            )

            if response.status_code != expected_status:
                request_args = (
                    path,
                    method,
                    creds,
                    "(follow_redirects=%s)" % follow_redirects,
                )
                actual_status = response.status_code
                failure = (request_args, expected_status, actual_status)
                failures.append(failure)

        if failures:
            msg = ""
            for (request_args, expected_status, actual_status) in failures:
                msg += (
                    "\n"
                    "Request:  %s\n"
                    "Expected: %s\n"
                    "Got:      %s\n" % (request_args, expected_status, actual_status)
                )

            self.fail("The following assertions failed:\n%s" % msg)


class TestDispatchingSiteRoot(DispatchingTestCase):
    def test_site_root_with_creds(self):
        expectations = [
            ("/", "GET", CREDS, 200),
            ("/", "POST", CREDS, 200),
            ("/", "PUT", CREDS, 200),
            ("/", "PATCH", CREDS, 200),
            ("/", "DELETE", CREDS, 200),
            ("/", "OPTIONS", CREDS, 200),
        ]
        self.validate(expectations)

    def test_site_root_without_creds(self):
        expectations = [
            ("/", "GET", NO_CREDS, 200),
            ("/", "POST", NO_CREDS, 401),
            ("/", "PUT", NO_CREDS, 401),
            ("/", "PATCH", NO_CREDS, 401),
            ("/", "DELETE", NO_CREDS, 401),
            ("/", "OPTIONS", NO_CREDS, 200),
        ]
        self.validate(expectations)

    def test_site_root_invalid_creds(self):
        expectations = [
            ("/", "GET", INVALID_CREDS, 200),
            ("/", "POST", INVALID_CREDS, 401),
            ("/", "PUT", INVALID_CREDS, 401),
            ("/", "PATCH", INVALID_CREDS, 401),
            ("/", "DELETE", INVALID_CREDS, 401),
            ("/", "OPTIONS", INVALID_CREDS, 200),
        ]
        self.validate(expectations)


class TestDispatchingNonExistentResource(DispatchingTestCase):
    def test_not_found_with_creds(self):
        expectations = [
            ("/not-found", "GET", CREDS, 404),
            ("/not-found", "POST", CREDS, 404),
            ("/not-found", "PUT", CREDS, 404),
            ("/not-found", "PATCH", CREDS, 404),
            ("/not-found", "DELETE", CREDS, 404),
            ("/not-found", "OPTIONS", CREDS, 404),
        ]
        self.validate(expectations)

    def test_not_found_without_creds(self):
        expectations = [
            ("/not-found", "GET", NO_CREDS, 404),
            ("/not-found", "POST", NO_CREDS, 404),
            ("/not-found", "PUT", NO_CREDS, 404),
            ("/not-found", "PATCH", NO_CREDS, 404),
            ("/not-found", "DELETE", NO_CREDS, 404),
            ("/not-found", "OPTIONS", NO_CREDS, 404),
        ]
        self.validate(expectations)

    def test_not_found_invalid_creds(self):
        expectations = [
            ("/not-found", "GET", INVALID_CREDS, 404),
            ("/not-found", "POST", INVALID_CREDS, 404),
            ("/not-found", "PUT", INVALID_CREDS, 404),
            ("/not-found", "PATCH", INVALID_CREDS, 404),
            ("/not-found", "DELETE", INVALID_CREDS, 404),
            ("/not-found", "OPTIONS", INVALID_CREDS, 404),
        ]
        self.validate(expectations)


class TestDispatchingDexterity(DispatchingTestCase):
    def setUp(self):
        super(TestDispatchingDexterity, self).setUp()
        self.portal.invokeFactory("Folder", id="private")

        self.portal.invokeFactory("Folder", id="public")
        public_folder = self.portal.public
        wftool = getToolByName(self.portal, "portal_workflow")
        wftool.doActionFor(public_folder, "publish")

        transaction.commit()

    def test_private_dx_folder_with_creds(self):
        expectations = [
            ("/private", "GET", CREDS, 200),
            ("/private", "POST", CREDS, 200),
            ("/private", "PUT", CREDS, 200),
            ("/private", "PATCH", CREDS, 200),
            ("/private", "DELETE", CREDS, 200),
            ("/private", "OPTIONS", CREDS, 200),
        ]
        self.validate(expectations)

    def test_private_dx_folder_without_creds(self):
        expectations = [
            ("/private", "GET", NO_CREDS, 401),
            ("/private", "POST", NO_CREDS, 401),
            ("/private", "PUT", NO_CREDS, 401),
            ("/private", "PATCH", NO_CREDS, 401),
            ("/private", "DELETE", NO_CREDS, 401),
            ("/private", "OPTIONS", NO_CREDS, 401),
        ]
        self.validate(expectations)

    def test_private_dx_folder_invalid_creds(self):
        expectations = [
            ("/private", "GET", INVALID_CREDS, 401),
            ("/private", "POST", INVALID_CREDS, 401),
            ("/private", "PUT", INVALID_CREDS, 401),
            ("/private", "PATCH", INVALID_CREDS, 401),
            ("/private", "DELETE", INVALID_CREDS, 401),
            ("/private", "OPTIONS", INVALID_CREDS, 401),
        ]
        self.validate(expectations)

    def test_public_dx_folder_with_creds(self):
        expectations = [
            ("/public", "GET", CREDS, 200),
            ("/public", "POST", CREDS, 200),
            ("/public", "PUT", CREDS, 200),
            ("/public", "PATCH", CREDS, 200),
            ("/public", "DELETE", CREDS, 200),
            ("/public", "OPTIONS", CREDS, 200),
        ]
        self.validate(expectations)

    def test_public_dx_folder_without_creds(self):
        expectations = [
            ("/public", "GET", NO_CREDS, 200),
            ("/public", "POST", NO_CREDS, 401),
            ("/public", "PUT", NO_CREDS, 401),
            ("/public", "PATCH", NO_CREDS, 401),
            ("/public", "DELETE", NO_CREDS, 401),
            ("/public", "OPTIONS", NO_CREDS, 200),
        ]
        self.validate(expectations)

    def test_public_dx_folder_invalid_creds(self):
        expectations = [
            ("/public", "GET", INVALID_CREDS, 200),
            ("/public", "POST", INVALID_CREDS, 401),
            ("/public", "PUT", INVALID_CREDS, 401),
            ("/public", "PATCH", INVALID_CREDS, 401),
            ("/public", "DELETE", INVALID_CREDS, 401),
            ("/public", "OPTIONS", INVALID_CREDS, 200),
        ]
        self.validate(expectations)


class TestDispatchingRedirects(DispatchingTestCase):
    def setUp(self):
        super(TestDispatchingRedirects, self).setUp()

        self.portal.invokeFactory("Folder", id="private-old")
        self.portal.manage_renameObject("private-old", "private-new")

        self.portal.invokeFactory("Folder", id="public-old")
        public_folder = self.portal["public-old"]
        wftool = getToolByName(self.portal, "portal_workflow")
        wftool.doActionFor(public_folder, "publish")
        self.portal.manage_renameObject("public-old", "public-new")

        transaction.commit()

    def test_moved_private_dx_folder_with_creds(self):
        expectations = [
            ("/private-old", "GET", CREDS, 301),
            ("/private-old", "POST", CREDS, 308),
            ("/private-old", "PUT", CREDS, 308),
            ("/private-old", "PATCH", CREDS, 308),
            ("/private-old", "DELETE", CREDS, 308),
            ("/private-old", "OPTIONS", CREDS, 308),
        ]
        self.validate(expectations)

        # Same, but with following redirects, asserting on the final status
        expectations = [
            ("/private-old", "GET", CREDS, 200),
            ("/private-old", "POST", CREDS, 200),
            ("/private-old", "PUT", CREDS, 200),
            ("/private-old", "PATCH", CREDS, 200),
            ("/private-old", "DELETE", CREDS, 200),
            ("/private-old", "OPTIONS", CREDS, 200),
        ]
        self.validate(expectations, follow_redirects=True)

    def test_moved_private_dx_folder_without_creds(self):
        expectations = [
            ("/private-old", "GET", NO_CREDS, 301),
            ("/private-old", "POST", NO_CREDS, 308),
            ("/private-old", "PUT", NO_CREDS, 308),
            ("/private-old", "PATCH", NO_CREDS, 308),
            ("/private-old", "DELETE", NO_CREDS, 308),
            ("/private-old", "OPTIONS", NO_CREDS, 308),
        ]
        self.validate(expectations)

        # Same, but with following redirects, asserting on the final status
        expectations = [
            ("/private-old", "GET", NO_CREDS, 401),
            ("/private-old", "POST", NO_CREDS, 401),
            ("/private-old", "PUT", NO_CREDS, 401),
            ("/private-old", "PATCH", NO_CREDS, 401),
            ("/private-old", "DELETE", NO_CREDS, 401),
            ("/private-old", "OPTIONS", NO_CREDS, 401),
        ]
        self.validate(expectations, follow_redirects=True)

    def test_moved_private_dx_folder_invalid_creds(self):
        expectations = [
            ("/private-old", "GET", INVALID_CREDS, 301),
            ("/private-old", "POST", INVALID_CREDS, 308),
            ("/private-old", "PUT", INVALID_CREDS, 308),
            ("/private-old", "PATCH", INVALID_CREDS, 308),
            ("/private-old", "DELETE", INVALID_CREDS, 308),
            ("/private-old", "OPTIONS", INVALID_CREDS, 308),
        ]
        self.validate(expectations)

        # Same, but with following redirects, asserting on the final status
        expectations = [
            ("/private-old", "GET", INVALID_CREDS, 401),
            ("/private-old", "POST", INVALID_CREDS, 401),
            ("/private-old", "PUT", INVALID_CREDS, 401),
            ("/private-old", "PATCH", INVALID_CREDS, 401),
            ("/private-old", "DELETE", INVALID_CREDS, 401),
            ("/private-old", "OPTIONS", INVALID_CREDS, 401),
        ]
        self.validate(expectations, follow_redirects=True)

    def test_moved_public_dx_folder_with_creds(self):
        expectations = [
            ("/public-old", "GET", CREDS, 301),
            ("/public-old", "POST", CREDS, 308),
            ("/public-old", "PUT", CREDS, 308),
            ("/public-old", "PATCH", CREDS, 308),
            ("/public-old", "DELETE", CREDS, 308),
            ("/public-old", "OPTIONS", CREDS, 308),
        ]
        self.validate(expectations)

        # Same, but with following redirects, asserting on the final status
        expectations = [
            ("/public-old", "GET", CREDS, 200),
            ("/public-old", "POST", CREDS, 200),
            ("/public-old", "PUT", CREDS, 200),
            ("/public-old", "PATCH", CREDS, 200),
            ("/public-old", "DELETE", CREDS, 200),
            ("/public-old", "OPTIONS", CREDS, 200),
        ]
        self.validate(expectations, follow_redirects=True)

    def test_moved_public_dx_folder_without_creds(self):
        expectations = [
            ("/public-old", "GET", NO_CREDS, 301),
            ("/public-old", "POST", NO_CREDS, 308),
            ("/public-old", "PUT", NO_CREDS, 308),
            ("/public-old", "PATCH", NO_CREDS, 308),
            ("/public-old", "DELETE", NO_CREDS, 308),
            ("/public-old", "OPTIONS", NO_CREDS, 308),
        ]
        self.validate(expectations)

        # Same, but with following redirects, asserting on the final status
        expectations = [
            ("/public-old", "GET", NO_CREDS, 200),
            ("/public-old", "POST", NO_CREDS, 401),
            ("/public-old", "PUT", NO_CREDS, 401),
            ("/public-old", "PATCH", NO_CREDS, 401),
            ("/public-old", "DELETE", NO_CREDS, 401),
            ("/public-old", "OPTIONS", NO_CREDS, 200),
        ]
        self.validate(expectations, follow_redirects=True)

    def test_moved_public_dx_folder_invalid_creds(self):
        expectations = [
            ("/public-old", "GET", INVALID_CREDS, 301),
            ("/public-old", "POST", INVALID_CREDS, 308),
            ("/public-old", "PUT", INVALID_CREDS, 308),
            ("/public-old", "PATCH", INVALID_CREDS, 308),
            ("/public-old", "DELETE", INVALID_CREDS, 308),
            ("/public-old", "OPTIONS", INVALID_CREDS, 308),
        ]
        self.validate(expectations)

        # Same, but with following redirects, asserting on the final status
        expectations = [
            ("/public-old", "GET", INVALID_CREDS, 200),
            ("/public-old", "POST", INVALID_CREDS, 401),
            ("/public-old", "PUT", INVALID_CREDS, 401),
            ("/public-old", "PATCH", INVALID_CREDS, 401),
            ("/public-old", "DELETE", INVALID_CREDS, 401),
            ("/public-old", "OPTIONS", INVALID_CREDS, 200),
        ]
        self.validate(expectations, follow_redirects=True)

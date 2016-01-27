# -*- coding: utf-8 -*-
from plone.app.testing import SITE_OWNER_NAME
from plone.app.testing import SITE_OWNER_PASSWORD
from plone.rest.testing import PLONE_REST_FUNCTIONAL_TESTING
from Products.CMFCore.utils import getToolByName

import requests
import transaction
import unittest


CREDS = (SITE_OWNER_NAME, SITE_OWNER_PASSWORD)
INVALID_CREDS = ('invalid', 'password')
NO_CREDS = ()


class DispatchingTestCase(unittest.TestCase):

    layer = PLONE_REST_FUNCTIONAL_TESTING

    def setUp(self):
        self.app = self.layer['app']
        self.request = self.layer['request']
        self.portal = self.layer['portal']
        self.portal_url = self.portal.absolute_url()

    def validate(self, expectations):
        failures = []
        for expectation in expectations:
            path, method, creds, expected_status = expectation
            url = self.portal_url + path

            response = requests.request(
                method, url,
                headers={'Accept': 'application/json'},
                auth=creds,
            )

            if response.status_code != expected_status:
                request_args = (path, method, creds)
                actual_status = response.status_code
                failure = (request_args, expected_status, actual_status)
                failures.append(failure)

        if failures:
            msg = ''
            for (request_args, expected_status, actual_status) in failures:
                msg += ('\n'
                        'Request:  %s\n'
                        'Expected: %s\n'
                        'Got:      %s\n' % (
                            request_args, expected_status, actual_status))

            self.fail('The following assertions failed:\n%s' % msg)


class TestDispatchingSiteRoot(DispatchingTestCase):

    def test_site_root_with_creds(self):
        expectations = [
            ('/', 'GET', CREDS, 200),
            ('/', 'POST', CREDS, 200),
            ('/', 'PUT', CREDS, 200),
            ('/', 'PATCH', CREDS, 200),
            ('/', 'DELETE', CREDS, 200),
            ('/', 'OPTIONS', CREDS, 200),
        ]
        self.validate(expectations)

    def test_site_root_without_creds(self):
        expectations = [
            ('/', 'GET', NO_CREDS, 200),
            ('/', 'POST', NO_CREDS, 401),
            ('/', 'PUT', NO_CREDS, 401),
            ('/', 'PATCH', NO_CREDS, 401),
            ('/', 'DELETE', NO_CREDS, 401),
            ('/', 'OPTIONS', NO_CREDS, 200),
        ]
        self.validate(expectations)

    def test_site_root_invalid_creds(self):
        expectations = [
            ('/', 'GET', INVALID_CREDS, 200),
            ('/', 'POST', INVALID_CREDS, 401),
            ('/', 'PUT', INVALID_CREDS, 401),
            ('/', 'PATCH', INVALID_CREDS, 401),
            ('/', 'DELETE', INVALID_CREDS, 401),
            ('/', 'OPTIONS', INVALID_CREDS, 200),
        ]
        self.validate(expectations)


class TestDispatchingNonExistentResource(DispatchingTestCase):

    def test_not_found_with_creds(self):
        expectations = [
            ('/not-found', 'GET', CREDS, 404),
            ('/not-found', 'POST', CREDS, 404),
            ('/not-found', 'PUT', CREDS, 404),
            ('/not-found', 'PATCH', CREDS, 404),
            ('/not-found', 'DELETE', CREDS, 404),
            ('/not-found', 'OPTIONS', CREDS, 404),
        ]
        self.validate(expectations)

    def test_not_found_without_creds(self):
        expectations = [
            ('/not-found', 'GET', NO_CREDS, 404),
            ('/not-found', 'POST', NO_CREDS, 404),
            ('/not-found', 'PUT', NO_CREDS, 404),
            ('/not-found', 'PATCH', NO_CREDS, 404),
            ('/not-found', 'DELETE', NO_CREDS, 404),
            ('/not-found', 'OPTIONS', NO_CREDS, 404),
        ]
        self.validate(expectations)

    def test_not_found_invalid_creds(self):
        expectations = [
            ('/not-found', 'GET', INVALID_CREDS, 404),
            ('/not-found', 'POST', INVALID_CREDS, 404),
            ('/not-found', 'PUT', INVALID_CREDS, 404),
            ('/not-found', 'PATCH', INVALID_CREDS, 404),
            ('/not-found', 'DELETE', INVALID_CREDS, 404),
            ('/not-found', 'OPTIONS', INVALID_CREDS, 404),
        ]
        self.validate(expectations)


class TestDispatchingDexterity(DispatchingTestCase):

    def setUp(self):
        super(TestDispatchingDexterity, self).setUp()
        self.portal.invokeFactory('Folder', id='private')

        self.portal.invokeFactory('Folder', id='public')
        public_folder = self.portal.public
        wftool = getToolByName(self.portal, "portal_workflow")
        wftool.doActionFor(public_folder, "publish")

        transaction.commit()

    def test_private_dx_folder_with_creds(self):
        expectations = [
            ('/private', 'GET', CREDS, 200),
            ('/private', 'POST', CREDS, 200),
            ('/private', 'PUT', CREDS, 200),
            ('/private', 'PATCH', CREDS, 200),
            ('/private', 'DELETE', CREDS, 200),
            ('/private', 'OPTIONS', CREDS, 200),
        ]
        self.validate(expectations)

    def test_private_dx_folder_without_creds(self):
        expectations = [
            ('/private', 'GET', NO_CREDS, 401),
            ('/private', 'POST', NO_CREDS, 401),
            ('/private', 'PUT', NO_CREDS, 401),
            ('/private', 'PATCH', NO_CREDS, 401),
            ('/private', 'DELETE', NO_CREDS, 401),
            ('/private', 'OPTIONS', NO_CREDS, 401),
        ]
        self.validate(expectations)

    def test_private_dx_folder_invalid_creds(self):
        expectations = [
            ('/private', 'GET', INVALID_CREDS, 401),
            ('/private', 'POST', INVALID_CREDS, 401),
            ('/private', 'PUT', INVALID_CREDS, 401),
            ('/private', 'PATCH', INVALID_CREDS, 401),
            ('/private', 'DELETE', INVALID_CREDS, 401),
            ('/private', 'OPTIONS', INVALID_CREDS, 401),
        ]
        self.validate(expectations)

    def test_public_dx_folder_with_creds(self):
        expectations = [
            ('/public', 'GET', CREDS, 200),
            ('/public', 'POST', CREDS, 200),
            ('/public', 'PUT', CREDS, 200),
            ('/public', 'PATCH', CREDS, 200),
            ('/public', 'DELETE', CREDS, 200),
            ('/public', 'OPTIONS', CREDS, 200),
        ]
        self.validate(expectations)

    def test_public_dx_folder_without_creds(self):
        expectations = [
            ('/public', 'GET', NO_CREDS, 200),
            ('/public', 'POST', NO_CREDS, 401),
            ('/public', 'PUT', NO_CREDS, 401),
            ('/public', 'PATCH', NO_CREDS, 401),
            ('/public', 'DELETE', NO_CREDS, 401),
            ('/public', 'OPTIONS', NO_CREDS, 200),
        ]
        self.validate(expectations)

    def test_public_dx_folder_invalid_creds(self):
        expectations = [
            ('/public', 'GET', INVALID_CREDS, 200),
            ('/public', 'POST', INVALID_CREDS, 401),
            ('/public', 'PUT', INVALID_CREDS, 401),
            ('/public', 'PATCH', INVALID_CREDS, 401),
            ('/public', 'DELETE', INVALID_CREDS, 401),
            ('/public', 'OPTIONS', INVALID_CREDS, 200),
        ]
        self.validate(expectations)

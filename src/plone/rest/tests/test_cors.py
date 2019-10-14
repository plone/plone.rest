# -*- coding: utf-8 -*-
from ZPublisher.pubevents import PubStart
from plone.app.testing import popGlobalRegistry
from plone.app.testing import pushGlobalRegistry
from plone.rest.cors import CORSPolicy
from plone.rest.interfaces import ICORSPolicy
from plone.rest.testing import PLONE_REST_INTEGRATION_TESTING
from zExceptions import Unauthorized
from zope.component import provideAdapter
from zope.event import notify
from zope.interface import Interface
from zope.publisher.interfaces.browser import IDefaultBrowserLayer

import unittest


class TestCORSPolicy(unittest.TestCase):

    layer = PLONE_REST_INTEGRATION_TESTING

    def setUp(self):
        self.request = self.layer["request"]
        self.response = self.request.response

    def get_policy(self, origin=None, method=None, headers=None):
        request = self.request
        if origin:
            request.environ["HTTP_ORIGIN"] = origin
        if method:
            request.environ["HTTP_ACCESS_CONTROL_REQUEST_METHOD"] = method
        if headers:
            request.environ["HTTP_ACCESS_CONTROL_REQUEST_HEADERS"] = headers
        policy = CORSPolicy(None, request)
        policy.allow_origin = ["*"]
        policy.allow_credentials = False
        policy.allow_methods = ["DELETE", "GET", "OPTIONS", "PATCH", "POST", "PUT"]
        policy.allow_headers = []
        policy.expose_headers = []
        policy.max_age = None
        return policy

    def test_simple_cors_without_origin_doesnt_add_ac_headers(self):
        policy = self.get_policy()
        self.assertFalse(policy.process_simple_request())
        self.assertEqual(None, self.response.getHeader("Access-Control-Allow-Origin"))

    def test_simple_cors_with_wrong_origin_doesnt_add_ac_headers(self):
        policy = self.get_policy(origin="http://wrong.net")
        policy.allow_origin = ["http://example.net"]
        self.assertFalse(policy.process_simple_request())
        self.assertEqual(None, self.response.getHeader("Access-Control-Allow-Origin"))

    def test_simple_cors_adds_wildcard_allow_origin(self):
        policy = self.get_policy(origin="http://example.net")
        self.assertTrue(policy.process_simple_request())
        self.assertEqual("*", self.response.getHeader("Access-Control-Allow-Origin"))

    def test_simple_cors_adds_matching_allow_origin(self):
        policy = self.get_policy(origin="http://example.net")
        policy.allow_origin = ["http://example.net"]
        self.assertTrue(policy.process_simple_request())
        self.assertEqual(
            "http://example.net", self.response.getHeader("Access-Control-Allow-Origin")
        )

    def test_simple_cors_adds_allow_credentials(self):
        policy = self.get_policy(origin="http://example.net")
        policy.allow_origin = ["http://example.net"]
        policy.allow_credentials = True
        self.assertTrue(policy.process_simple_request())
        self.assertEqual(
            "true", self.response.getHeader("Access-Control-Allow-Credentials")
        )

    def test_simple_cors_adds_origin_when_supporting_credentials(self):
        policy = self.get_policy(origin="http://example.net")
        policy.allow_credentials = True
        self.assertTrue(policy.process_simple_request())
        self.assertEqual(
            "http://example.net", self.response.getHeader("Access-Control-Allow-Origin")
        )
        self.assertEqual(
            "true", self.response.getHeader("Access-Control-Allow-Credentials")
        )

    def test_simple_cors_adds_vary_when_allowing_multiple_origins(self):
        policy = self.get_policy(origin="http://example.net")
        policy.allow_origin = ["http://some.host", "http://example.net"]
        self.assertTrue(policy.process_simple_request())
        self.assertEqual("Origin", self.response.getHeader("Vary"))

    def test_simple_cors_adds_exposed_headers(self):
        policy = self.get_policy(origin="http://example.net")
        policy.expose_headers = ["Content-Length", "X-My-Header"]
        self.assertTrue(policy.process_simple_request())
        self.assertEqual(
            "Content-Length, X-My-Header",
            self.response.getHeader("Access-Control-Expose-Headers"),
        )

    def test_preflight_cors_without_origin_doesnt_add_ac_headers(self):
        policy = self.get_policy()
        self.assertFalse(policy.process_preflight_request())
        self.assertEqual(None, self.response.getHeader("Access-Control-Allow-Origin"))

    def test_preflight_cors_with_wrong_origin_doesnt_add_ac_headers(self):
        policy = self.get_policy(origin="http://wrong.net")
        policy.allow_origin = ["http://example.net"]
        self.assertFalse(policy.process_preflight_request())
        self.assertEqual(None, self.response.getHeader("Access-Control-Allow-Origin"))

    def test_preflight_cors_with_wrong_method_doesnt_add_ac_headers(self):
        policy = self.get_policy(origin="http://example.net", method="LOCK")
        self.assertFalse(policy.process_preflight_request())
        self.assertEqual(None, self.response.getHeader("Access-Control-Allow-Origin"))

    def test_preflight_cors_with_wrong_header_doesnt_add_ac_headers(self):
        policy = self.get_policy(origin="http://example.net", headers="X-Secret")
        self.assertFalse(policy.process_preflight_request())
        self.assertEqual(None, self.response.getHeader("Access-Control-Allow-Origin"))

    def test_preflight_cors_adds_wildcard_allow_origin(self):
        policy = self.get_policy(origin="http://example.net", method="GET")
        self.assertTrue(policy.process_preflight_request())
        self.assertEqual("*", self.response.getHeader("Access-Control-Allow-Origin"))

    def test_preflight_cors_adds_matching_allow_origin(self):
        policy = self.get_policy(origin="http://example.net", method="GET")
        policy.allow_origin = ["http://example.net"]
        self.assertTrue(policy.process_preflight_request())
        self.assertEqual(
            "http://example.net", self.response.getHeader("Access-Control-Allow-Origin")
        )

    def test_preflight_cors_adds_allow_credentials(self):
        policy = self.get_policy(origin="http://example.net", method="GET")
        policy.allow_origin = ["http://example.net"]
        policy.allow_credentials = True
        self.assertTrue(policy.process_preflight_request())
        self.assertEqual(
            "true", self.response.getHeader("Access-Control-Allow-Credentials")
        )

    def test_preflight_cors_adds_origin_when_supporting_credentials(self):
        policy = self.get_policy(origin="http://example.net", method="GET")
        policy.allow_credentials = True
        self.assertTrue(policy.process_preflight_request())
        self.assertEqual(
            "http://example.net", self.response.getHeader("Access-Control-Allow-Origin")
        )
        self.assertEqual(
            "true", self.response.getHeader("Access-Control-Allow-Credentials")
        )

    def test_preflight_cors_adds_vary_when_allowing_multiple_origins(self):
        policy = self.get_policy(origin="http://example.net", method="GET")
        policy.allow_origin = ["http://some.host", "http://example.net"]
        self.assertTrue(policy.process_preflight_request())
        self.assertEqual("Origin", self.response.getHeader("Vary"))

    def test_preflight_cors_adds_max_age(self):
        policy = self.get_policy(origin="http://example.net", method="GET")
        policy.max_age = "3600"
        self.assertTrue(policy.process_preflight_request())
        self.assertEqual("3600", self.response.getHeader("Access-Control-Max-Age"))

    def test_preflight_cors_adds_allow_methods(self):
        policy = self.get_policy(origin="http://example.net", method="GET")
        self.assertTrue(policy.process_preflight_request())
        self.assertEqual("GET", self.response.getHeader("Access-Control-Allow-Methods"))

    def test_preflight_cors_adds_allow_methods_if_unrestriced(self):
        policy = self.get_policy(origin="http://example.net", method="GET")
        policy.allow_methods = None
        self.assertTrue(policy.process_preflight_request())
        self.assertEqual("GET", self.response.getHeader("Access-Control-Allow-Methods"))

    def test_preflight_cors_adds_allow_headers(self):
        policy = self.get_policy(origin="http://example.net", method="GET")
        policy.allow_headers = ["X-Allowed"]
        self.assertTrue(policy.process_preflight_request())
        self.assertEqual(
            "X-Allowed", self.response.getHeader("Access-Control-Allow-Headers")
        )

    def test_preflight_cors_sets_content_length_zero(self):
        policy = self.get_policy(origin="http://example.net", method="GET")
        self.assertTrue(policy.process_preflight_request())
        self.assertEqual("0", self.response.getHeader("Content-Length"))

    def test_preflight_cors_sets_status_code_200(self):
        policy = self.get_policy(origin="http://example.net", method="GET")
        self.assertTrue(policy.process_preflight_request())
        self.assertEqual(200, self.response.getStatus())


class TestCORS(unittest.TestCase):

    layer = PLONE_REST_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        self.request = self.layer["request"]

    def traverse(self, path="/plone", method="GET", headers={}):
        request = self.layer["request"]
        request.environ["PATH_INFO"] = path
        request.environ["PATH_TRANSLATED"] = path
        request.environ["REQUEST_METHOD"] = method
        request.environ["HTTP_ORIGIN"] = "http://example.net"
        request.environ.update(headers)
        notify(PubStart(request))
        return request.traverse(path)

    def test_preflight_cors_is_accessible_anonymously(self):
        headers = {}
        headers["HTTP_ACCESS_CONTROL_REQUEST_METHOD"] = "POST"
        try:
            self.traverse(method="OPTIONS", headers=headers)
        except Unauthorized:
            self.fail("Service not accessible for preflight.")

    def test_simple_cors_gets_processed(self):
        headers = {}
        headers["HTTP_ACCEPT"] = "application/json"
        obj = self.traverse(method="GET", headers=headers)
        obj()
        self.assertEqual(
            "*", self.request.response.getHeader("Access-Control-Allow-Origin")
        )

    def test_preflight_request_without_cors_policy_doesnt_render_service(self):
        # "Unregister" the current CORS policy
        class NoCORSPolicy(object):
            def __new__(cls, context, request):
                return None

        pushGlobalRegistry(self.portal)
        provideAdapter(NoCORSPolicy, (Interface, IDefaultBrowserLayer), ICORSPolicy)

        headers = {"HTTP_ACCESS_CONTROL_REQUEST_METHOD": "GET", "HTTP_ACCEPT": "*/*"}
        service = self.traverse(method="OPTIONS", headers=headers)
        self.assertTrue(service() is None, "Should return None")

        popGlobalRegistry(self.portal)

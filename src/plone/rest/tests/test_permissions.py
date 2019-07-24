# -*- coding: utf-8 -*-
from Products.CMFCore.utils import getToolByName
from ZPublisher.pubevents import PubStart
from base64 import b64encode
from plone.app.testing import SITE_OWNER_NAME
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import TEST_USER_PASSWORD
from plone.app.testing import login
from plone.app.testing import setRoles
from plone.rest.service import Service
from plone.rest.testing import PLONE_REST_INTEGRATION_TESTING
from zExceptions import Unauthorized
from zope.event import notify

import unittest


class TestPermissions(unittest.TestCase):

    layer = PLONE_REST_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        self.request = self.layer["request"]
        setRoles(self.portal, TEST_USER_ID, ["Member"])
        self.portal.acl_users.userFolderAddUser("admin", "secret", ["Manager"], [])
        login(self.portal, SITE_OWNER_NAME)
        self.portal.invokeFactory("Document", id="doc1")
        wftool = getToolByName(self.portal, "portal_workflow")
        wftool.doActionFor(self.portal.doc1, "publish")

    def traverse(self, path="/plone", accept="application/json", method="GET"):
        request = self.layer["request"]
        request.environ["PATH_INFO"] = path
        request.environ["PATH_TRANSLATED"] = path
        request.environ["HTTP_ACCEPT"] = accept
        request.environ["REQUEST_METHOD"] = method
        auth = "%s:%s" % (TEST_USER_NAME, TEST_USER_PASSWORD)
        b64auth = b64encode(auth.encode("utf8"))
        request._auth = "Basic %s" % b64auth.decode("utf8")
        notify(PubStart(request))
        return request.traverse(path)

    def test_traverse_with_insufficient_permission_raises_unauthorized(self):
        setRoles(self.portal, TEST_USER_ID, ["Member"])
        with self.assertRaises(Unauthorized):
            self.traverse("/plone/doc1", method="PUT")

    def test_traverse_with_sufficient_permission_returns_service(self):
        setRoles(self.portal, TEST_USER_ID, ["Editor"])
        obj = self.traverse("/plone/doc1", method="PUT")
        self.assertTrue(isinstance(obj, Service), "Not a service")

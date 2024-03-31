from base64 import b64encode
from plone.app.layout.navigation.interfaces import INavigationRoot
from plone.app.testing import setRoles
from plone.app.testing import SITE_OWNER_NAME
from plone.app.testing import SITE_OWNER_PASSWORD
from plone.app.testing import TEST_USER_ID
from plone.rest.service import Service
from plone.rest.testing import PLONE_REST_INTEGRATION_TESTING
from Products.SiteAccess.VirtualHostMonster import VirtualHostMonster
from zExceptions import NotFound
from zExceptions import Redirect
from zope.event import notify
from zope.interface import alsoProvides
from zope.publisher.interfaces.browser import IBrowserView
from ZPublisher import BeforeTraverse
from ZPublisher.pubevents import PubStart

import unittest


class TestTraversal(unittest.TestCase):
    layer = PLONE_REST_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        self.request = self.layer["request"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

    def traverse(self, path="/plone", accept="application/json", method="GET"):
        request = self.layer["request"]
        request.environ["PATH_INFO"] = path
        request.environ["PATH_TRANSLATED"] = path
        request.environ["HTTP_ACCEPT"] = accept
        request.environ["REQUEST_METHOD"] = method
        auth = f"{SITE_OWNER_NAME}:{SITE_OWNER_PASSWORD}"
        b64auth = b64encode(auth.encode("utf8"))
        request._auth = "Basic %s" % b64auth.decode("utf8")
        notify(PubStart(request))
        return request.traverse(path)

    def test_json_request_on_portal_root_returns_service(self):
        obj = self.traverse()
        self.assertTrue(isinstance(obj, Service), "Not a service")

    def test_json_request_on_portal_root_with_layout_returns_service(self):
        self.portal.setLayout("summary_view")
        obj = self.traverse()
        self.assertTrue(isinstance(obj, Service), "Not a service")

    def test_json_request_on_portal_root_with_default_page_returns_service(self):
        self.portal.invokeFactory("Document", id="doc1")
        self.portal.setDefaultPage("doc1")
        obj = self.traverse()
        self.assertTrue(isinstance(obj, Service), "Not a service")

    def test_json_request_on_content_object_returns_service(self):
        self.portal.invokeFactory("Document", id="doc1")
        obj = self.traverse(path="/plone/doc1")
        self.assertTrue(isinstance(obj, Service), "Not a service")

    def test_html_request_on_portal_root_returns_default_view(self):
        obj = self.traverse(accept="text/html")
        self.assertEqual(self.portal.getDefaultLayout(), obj.__name__)

    def test_html_request_on_portal_root_returns_dynamic_view(self):
        self.portal.setLayout("summary_view")
        obj = self.traverse(accept="text/html")
        self.assertEqual("summary_view", obj.__name__)

    def test_html_request_on_portal_root_returns_default_page(self):
        self.portal.invokeFactory("Document", id="doc1")
        self.portal.setDefaultPage("doc1")
        obj = self.traverse(accept="text/html")
        self.assertEqual("document_view", obj.__name__)

    def test_json_request_on_object_with_multihook(self):
        doc1 = self.portal[self.portal.invokeFactory("Document", id="doc1")]

        # Register a function to be called before traversal
        def btr_test(container, request):
            request._btr_test_called = 1

        doc1.btr_test = btr_test
        nc = BeforeTraverse.NameCaller("btr_test")
        BeforeTraverse.registerBeforeTraverse(doc1, nc, "Document/btr_test")

        obj = self.traverse(path="/plone/doc1")
        self.assertTrue(isinstance(obj, Service), "Not a service")
        self.assertEqual(1, self.request._btr_test_called)

    def test_json_request_on_existing_view_returns_named_service(self):
        obj = self.traverse("/plone/search")
        self.assertTrue(isinstance(obj, Service), "Not a service")

        folder = self.portal[self.portal.invokeFactory("Folder", id="folder1")]
        alsoProvides(folder, INavigationRoot)
        obj = self.traverse("/plone/folder1/search")
        self.assertTrue(isinstance(obj, Service), "Not a service")

    def test_html_request_on_existing_view_returns_view(self):
        obj = self.traverse(path="/plone/search", accept="text/html")
        self.assertFalse(isinstance(obj, Service), "Got a service")

        folder = self.portal[self.portal.invokeFactory("Folder", id="folder1")]
        alsoProvides(folder, INavigationRoot)
        obj = self.traverse(path="/plone/folder1/search", accept="text/html")
        self.assertFalse(isinstance(obj, Service), "Got a service")

    def test_html_request_via_api_returns_service(self):
        obj = self.traverse(path="/plone/++api++", accept="text/html")
        self.assertTrue(isinstance(obj, Service), "Not a service")

    def test_html_request_via_double_apis_raises_redirect(self):
        portal_url = self.portal.absolute_url()
        with self.assertRaises(Redirect) as exc:
            self.traverse(path="/plone/++api++/++api++", accept="text/html")
        self.assertEqual(
            exc.exception.headers["Location"],
            f"{portal_url}/++api++",
        )

    def test_html_request_via_multiple_apis_raises_redirect(self):
        portal_url = self.portal.absolute_url()
        with self.assertRaises(Redirect) as exc:
            self.traverse(
                path="/plone/++api++/++api++/++api++/search", accept="text/html"
            )
        self.assertEqual(
            exc.exception.headers["Location"],
            f"{portal_url}/++api++/search",
        )

    def test_html_request_via_multiple_bad_apis_raises_not_found(self):
        with self.assertRaises(NotFound):
            self.traverse(path="/plone/++api++/search/++api++", accept="text/html")

    def test_virtual_hosting(self):
        app = self.layer["app"]
        vhm = VirtualHostMonster()
        vhm.id = "virtual_hosting"
        vhm.addToContainer(app)
        obj = self.traverse(
            path="/VirtualHostBase/http/localhost:8080/plone/VirtualHostRoot/"
        )  # noqa
        self.assertTrue(isinstance(obj, Service), "Not a service")
        del app["virtual_hosting"]

    def test_json_request_to_regular_view_returns_view(self):
        obj = self.traverse("/plone/folder_contents")
        self.assertTrue(IBrowserView.providedBy(obj), "IBrowserView expected")

        self.portal[self.portal.invokeFactory("Folder", id="folder1")]
        obj = self.traverse("/plone/folder1/folder_contents")
        self.assertTrue(IBrowserView.providedBy(obj), "IBrowserView expected")

    def test_json_request_to_view_namespace_returns_view(self):
        obj = self.traverse("/plone/@@folder_contents")
        self.assertTrue(IBrowserView.providedBy(obj), "IBrowserView expected")

        self.portal[self.portal.invokeFactory("Folder", id="folder1")]
        obj = self.traverse("/plone/folder1/@@folder_contents")
        self.assertTrue(IBrowserView.providedBy(obj), "IBrowserView expected")

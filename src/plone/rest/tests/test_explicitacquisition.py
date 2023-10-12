from base64 import b64encode
from plone.app.testing import setRoles
from plone.app.testing import SITE_OWNER_NAME
from plone.app.testing import SITE_OWNER_PASSWORD
from plone.app.testing import TEST_USER_ID
from plone.rest.testing import PLONE_REST_INTEGRATION_TESTING
from Products.CMFPlone import __version__
from zExceptions import NotFound
from zope.event import notify
from ZPublisher.pubevents import PubAfterTraversal
from ZPublisher.pubevents import PubStart

import unittest

try:
    from Products.CMFCore.explicitacquisition import SKIP_PTA
except ImportError:
    SKIP_PTA = None


@unittest.skipUnless(
    SKIP_PTA is None,
    "Older Plone versions don't have CMFCore>=3.2",
)
class TestExplicitAcquisitionUnavailable(unittest.TestCase):
    layer = PLONE_REST_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        self.request = self.layer["request"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self.portal.invokeFactory("Document", id="foo")

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

    def test_portal_root(self):
        self.traverse("/plone")
        notify(PubAfterTraversal(self.request))

    def test_portal_foo(self):
        self.traverse("/plone/foo")
        notify(PubAfterTraversal(self.request))

    def test_portal_foo_acquired(self):
        self.traverse("/plone/foo/foo")
        notify(PubAfterTraversal(self.request))


@unittest.skipUnless(
    SKIP_PTA is not None,
    "We have Products.CMFPlone >= 3.2",
)
class TestExplicitAcquisitionAvailable(unittest.TestCase):
    layer = PLONE_REST_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        self.request = self.layer["request"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self.portal.invokeFactory("Document", id="foo")

    def traverse(self, path="/plone", accept="application/json", method="GET"):
        request = self.layer["request"]
        request.environ["PATH_INFO"] = path
        request.environ["PATH_TRANSLATED"] = path
        request.environ["HTTP_ACCEPT"] = accept
        request.environ["REQUEST_METHOD"] = method
        auth = "%s:%s" % (SITE_OWNER_NAME, SITE_OWNER_PASSWORD)
        b64auth = b64encode(auth.encode("utf8"))
        request._auth = "Basic %s" % b64auth.decode("utf8")
        notify(PubStart(request))
        return request.traverse(path)

    def test_portal_root(self):
        import Products.CMFCore.explicitacquisition

        self.traverse("/plone")
        Products.CMFCore.explicitacquisition.SKIP_PTA = True
        notify(PubAfterTraversal(self.request))

        Products.CMFCore.explicitacquisition.SKIP_PTA = False
        notify(PubAfterTraversal(self.request))

    def test_portal_foo(self):
        import Products.CMFCore.explicitacquisition

        self.traverse("/plone/foo")
        Products.CMFCore.explicitacquisition.SKIP_PTA = True
        notify(PubAfterTraversal(self.request))

        Products.CMFCore.explicitacquisition.SKIP_PTA = False
        notify(PubAfterTraversal(self.request))

    def test_portal_foo_acquired(self):
        import Products.CMFCore.explicitacquisition

        self.traverse("/plone/foo/foo")

        Products.CMFCore.explicitacquisition.SKIP_PTA = True
        notify(PubAfterTraversal(self.request))

        Products.CMFCore.explicitacquisition.SKIP_PTA = False
        with self.assertRaises(NotFound):
            notify(PubAfterTraversal(self.request))

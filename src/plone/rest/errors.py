from AccessControl import getSecurityManager

try:
    from plone.app.redirector.interfaces import IRedirectionStorage
except ImportError:
    IRedirectionStorage = None
from plone.memoize.instance import memoize
from plone.rest.interfaces import IAPIRequest
from plone.rest.interfaces import ICORSPolicy
from Products.CMFCore.permissions import ManagePortal
from Products.Five.browser import BrowserView
from six.moves import urllib
from six.moves.urllib.parse import quote
from six.moves.urllib.parse import unquote
from zExceptions import NotFound

try:
    from ZPublisher.HTTPRequest import WSGIRequest

    HAS_WSGI = True
except ImportError:
    HAS_WSGI = False
from zope.component import adapter
from zope.component import queryMultiAdapter
from zope.component import queryUtility
from zope.component.hooks import getSite

import json
import six
import sys
import traceback


@adapter(Exception, IAPIRequest)
class ErrorHandling(BrowserView):
    """This view is responsible for serializing unhandled exceptions, as well
    as handling 404 Not Found errors and redirects.
    """

    def __call__(self):
        exception = self.context
        data = self.render_exception(exception)
        result = json.dumps(data, indent=2, sort_keys=True)

        # Write and lock the response in order to avoid later changes
        # especially for Unauthorized exceptions.
        response = self.request.response
        response.setHeader("Content-Type", "application/json")
        response.setStatus(type(exception), lock=1)
        response.setBody(result, lock=1)

        # Avoid redirect to login page on Unauthorized by adding
        # a fake challenged flag, which makes the PAS believe it
        # already did challenge and redirect.
        response._has_challenged = True
        return

    def render_exception(self, exception):
        name = type(exception).__name__
        message = str(exception)
        if six.PY2:
            name = name.decode("utf-8")
            message = message.decode("utf-8")
        result = {u"type": name, u"message": message}

        policy = queryMultiAdapter((self.context, self.request), ICORSPolicy)
        if policy is not None:
            policy.process_simple_request()

        if isinstance(exception, NotFound):
            # First check if a redirect from p.a.redirector exists
            redirect_performed = self.attempt_redirect()
            if redirect_performed:
                self.request.response.setBody("", lock=1)
                return

            # NotFound exceptions need special handling because their
            # exception message gets turned into HTML by ZPublisher
            url = self.request.getURL()
            result[u"message"] = u"Resource not found: %s" % url

        if getSecurityManager().checkPermission(ManagePortal, getSite()):
            result[u"traceback"] = self.render_traceback(exception)

        return result

    def render_traceback(self, exception):
        _, exc_obj, exc_traceback = sys.exc_info()
        if exception is not exc_obj:
            if (
                HAS_WSGI
                and isinstance(self.request, WSGIRequest)
                and str(exception) == str(exc_obj)
            ):
                # WSGIRequest may "upgrade" the exception,
                # resulting in a new exception which has
                # the same string representation as the
                # original exception.
                # https://github.com/plone/Products.CMFPlone/issues/2474
                # https://github.com/plone/plone.rest/commit/96599cc3bb3ef5a23b10eb585781d88274fbcaf5#comments
                pass
            else:
                return (
                    u"ERROR: Another exception happened before we could "
                    u"render the traceback."
                )

        raw = "\n".join(traceback.format_tb(exc_traceback))
        return raw.strip().split("\n")

    def find_redirect_if_view_or_service(self, old_path_elements, storage):
        """Find redirect for URLs like:
        - http://example.com/object/namedservice/param
        - http://example.com/object/@@view/param
        - http://example.com/object/template

        This combines the functionality of the find_redirect_if_view() and
        find_redirect_if_template() methods of the original FourOhFourView into
        one, and also makes it support named services.

        For this to also work for named services we use a different strategy
        here: Based on old_path_elements, try to find the longest stored
        redirect (if any), and consider the remaining path parts the remainder
        (view, template, named services plus possible params) that will need
        to be appended to the new object path.
        """
        if len(old_path_elements) <= 1:
            return None

        # Parts to the left of the split point are considered a potential
        # object path, while the right part is the remainder. Starting from
        # the right (longest potential obj path), we keep moving the split
        # point to the left and look for shorter matches.
        #
        # Once we reach the point where the obj path is separated from the
        # remainder, we should get a match if there's a stored redirect.
        #
        # ['', 'Plone', 'folder', 'item', '@@view', 'param']
        #                                ^
        splitpoint = len(old_path_elements)

        while splitpoint > 1:
            possible_obj_path = "/".join(old_path_elements[:splitpoint])
            remainder = old_path_elements[splitpoint:]
            new_path = storage.get(possible_obj_path)

            if new_path:
                if new_path == possible_obj_path:
                    # New URL would match originally requested URL.
                    # Lets not cause a redirect loop.
                    return None
                return new_path + "/" + "/".join(remainder)

            splitpoint -= 1

        return None

    def attempt_redirect(self):
        """Check if a redirect is needed, and perform it if necessary.

        Returns True if a redirect has been performed, False otherwise.

        This method is based on FourOhFourView.attempt_redirect() from
        p.a.redirector. It's copied here because we want to answer redirects
        to non-GET methods with status 308, but since this method locks the
        response status, we wouldn't be able to change it afterwards.
        """
        url = self._url()
        if not url:
            return False

        try:
            old_path_elements = self.request.physicalPathFromURL(url)
        except ValueError:  # pragma: no cover
            return False  # pragma: no cover

        storage = queryUtility(IRedirectionStorage)
        if storage is None:
            return False

        old_path = "/".join(old_path_elements)

        # First lets try with query string in cases or content migration

        new_path = None

        query_string = self.request.QUERY_STRING
        if query_string:
            new_path = storage.get("%s?%s" % (old_path, query_string))
            # if we matched on the query_string we don't want to include it
            # in redirect
            if new_path:
                query_string = ""

        if not new_path:
            new_path = storage.get(old_path)

        # Attempt our own strategy at finding redirects for named REST
        # services, views or templates.
        if not new_path:
            new_path = self.find_redirect_if_view_or_service(old_path_elements, storage)

        if not new_path:
            return False

        url = urllib.parse.urlsplit(new_path)
        if url.netloc:
            # External URL
            # avoid double quoting
            url_path = unquote(url.path)
            url_path = quote(url_path)
            url = urllib.parse.SplitResult(*(url[:2] + (url_path,) + url[3:])).geturl()
        else:
            url = self.request.physicalPathToURL(new_path)

        # some analytics programs might use this info to track
        if query_string:
            url += "?" + query_string

        # Answer GET requests with 301. Every other method will be answered
        # with 308 Permanent Redirect, which instructs the client to NOT
        # switch the method (if the original request was a POST, it should
        # re-POST to the new URL from the Location header).
        if self.request.method.upper() == "GET":
            status = 301
        else:
            status = 308

        self.request.response.redirect(url, status=status, lock=1)
        return True

    @memoize
    def _url(self):
        """Get the current, canonical URL"""
        return self.request.get(
            "ACTUAL_URL",
            self.request.get(
                "VIRTUAL_URL", self.request.get("URL", None)  # noqa  # noqa
            ),
        )  # noqa

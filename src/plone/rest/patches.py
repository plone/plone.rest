# -*- coding: utf-8 -*-
from plone.rest.interfaces import IAPIRequest


def __before_publishing_traverse__(self, arg1, arg2=None):
    """Pre-traversal hook that stops traversal to prevent the default view
    to be appended. Appending the default view would break REST calls.
    """
    # XXX hack around a bug(?) in BeforeTraverse.MultiHook
    REQUEST = arg2 or arg1

    if IAPIRequest.providedBy(REQUEST):
        return

    return self._old___before_publishing_traverse__(arg1, arg2)


PERMANENT_REDIRECT = {308: "Permanent Redirect"}


def patch_zpublisher_status_codes(scope, unused_original, unused_replacement):
    """Add '308 Permanent Redirect' to the list of status codes the ZPublisher
    knows about. Otherwise setStatus() will turn it into a 500.

    This is needed for up to and including Plone 5.1.
    """
    status_reasons = getattr(scope, "status_reasons", {})
    if 308 in status_reasons:
        # Already present in zExceptions >= 3.2 / Zope >= 4.0a1 / Plone 5.2
        return

    # Patch the forward mapping (code -> reason)
    status_reasons.update(PERMANENT_REDIRECT)

    # Update the reverse mapping
    status_codes = getattr(scope, "status_codes", {})
    key, val = PERMANENT_REDIRECT.items()[0]

    status_codes["".join(val.split(" ")).lower()] = key
    status_codes[val.lower()] = key
    status_codes[key] = key
    status_codes[str(key)] = key

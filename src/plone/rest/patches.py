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

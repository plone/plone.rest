# -*- coding: utf-8 -*-
from zope.interface import Interface


class IAPIRequest(Interface):
    """Marker for API requests.
    """


class IService(Interface):
    """Marker for REST services.
    """

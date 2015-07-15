# -*- coding: utf-8 -*-
from zope.interface import Interface


class IGET(Interface):
    """ Get method
    """


class IPOST(Interface):
    """ Post method
    """


class IPUT(Interface):
    """ Put method
    """


class IDELETE(Interface):
    """ Delete method
    """


class IOPTIONS(Interface):
    """ Options method
    """


class IPATCH(Interface):
    """ Patch method
    """


class IAPIRequest(Interface):
    """Marker for API requests.
    """

# -*- coding: utf-8 -*-
from zope.configuration.exceptions import ConfigurationError
from zope.configuration.fields import GlobalObject
from zope.interface import Interface
from zope.schema import TextLine
from zope.publisher.interfaces.browser import IBrowserPublisher
from plone.rest import interfaces
<<<<<<< c9c03375f2f6957a0b416aedbfb9f417b50b8139
from plone.rest.cors import get_cors_preflight_view
from plone.rest.traverse import NAME_PREFIX
=======
from plone.rest.cors import wrap_cors, options_view
>>>>>>> initial implemention of cors

from zope.component.zcml import adapter
from zope.security.zcml import Permission
from zope.security.checker import CheckerPublic


class IService(Interface):
    """
    """

    method = TextLine(
        title=u"The name of the view that should be the default. " +
              u"[get|post|put|delete]",
        description=u"""
        This name refers to view that should be the view used by
        default (if no view name is supplied explicitly).""",
        )

    for_ = GlobalObject(
        title=u"The interface this view is the default for.",
        description=u"""Specifies the interface for which the view is
        registered. All objects implementing this interface can make use of
        this view. If this attribute is not specified, the view is available
        for all objects.""",
        )

    factory = GlobalObject(
        title=u"The factory for this service",
        description=u"The factory is usually subclass of the Service class.")

    name = TextLine(
        title=u"The name of the service.",
        description=u"""When no name is defined, the service is available at
        the object's absolute URL. When defining a name, the service is
        available at the object's absolute URL appended with a slash and the
        service name.""",
        required=False,
        default=u'')

    cors_enabled = Boolean(
        title=u"CORS enabled",
        description=u""" To use if you especially want to disable CORS support for a particular
        service / method.""",
        default=True
        )

    cors_origin = TextLine(
        title=u"CORS origin",
        description=u"""
        The list of origins for CORS. You can use wildcards here if needed,
        e.g. ('list', 'of', '*.domain').""",
        required=False,
        default=u'*'
        )

    cors_headers = Text(
        title=u"List of headers that are enabled on cors",
        description="The list of headers supported for the services",
        required=False
        )

    cors_expose_all_headers = TextLine(
        title=u"Expose all the headers",
        description=""" If set to True, all the headers will be exposed and considered valid
        ones (Default: True). If set to False, all the headers need be
        explicitly mentioned with the cors_headers parameter.""",
        required=False
        )

    permission = Permission(
        title=u"Permission",
        description=u"The permission needed to use the view.",
        required=False
        )


def serviceDirective(
        _context,
        method,
        factory,
        for_,
        name=u'',
        cors_enabled=False,
        layer=None,
        cors_origin=None,
        permission=CheckerPublic
        ):

    if method.upper() == 'GET':
        marker = interfaces.IGET
    elif method.upper() == 'POST':
        marker = interfaces.IPOST
    elif method.upper() == 'OPTIONS':
        marker = interfaces.IOPTIONS
    elif method.upper() == 'PUT':
        marker = interfaces.IPUT
    elif method.upper() == 'DELETE':
        marker = interfaces.IDELETE
    elif method.upper() == 'PATCH':
        marker = interfaces.IPATCH
    else:
        raise ConfigurationError(
            u"No implementation for %s method" % method
        )

    required = {}

    if permission == 'zope.Public':
        permission = CheckerPublic

    for n in ('browserDefault', '__call__', 'publishTraverse'):
        required[n] = permission

    # defineChecker(factory, Checker(required))

    if cors_origin:
        # Check if there is already an adapter for options

        adapter(
            _context,
            factory=(options_view(cors_origin),),
            provides=IBrowserPublisher,
            for_=(for_, interfaces.IOPTIONS),
            name=NAME_PREFIX + name
        )

        adapter(
            _context,
            factory=(wrap_cors(factory, cors_origin),),
            provides=IBrowserPublisher,
            for_=(for_, marker),
            name=NAME_PREFIX + name
        )

    adapter(
        _context,
        factory=(factory,),
        provides=IBrowserPublisher,
        for_=(for_, marker),
        name=NAME_PREFIX + name,
    )

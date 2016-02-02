# -*- coding: utf-8 -*-
from plone.rest.cors import get_cors_preflight_view
from plone.rest.negotiation import parse_accept_header
from plone.rest.negotiation import register_service
from zope.component.zcml import adapter
from zope.configuration.fields import GlobalInterface
from zope.configuration.fields import GlobalObject
from zope.interface import Interface
from zope.publisher.interfaces.browser import IBrowserPublisher
from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from zope.schema import TextLine, Bool
from zope.security.checker import CheckerPublic
from zope.security.zcml import Permission


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

    accept = TextLine(
        title=u"Acceptable media types",
        description=u"""Specifies the media type used for content negotiation.
        The service is limited to the given media type and only called if the
        request contains an "Accept" header with the given media type. Multiple
        media types can be given by separating them with a comma.""",
        default=u"application/json")

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

    layer = GlobalInterface(
        title=u"The browser layer for which this service is registered.",
        description=u"""Useful for overriding existing services or for making
                        services available only if a specific add-on has been
                        installed.""",
        required=False,
        default=IDefaultBrowserLayer,
        )

    cors_enabled = Bool(
        title=u"The name of the view that should be the default."
              u"[get|post|put|delete]",
        description=u"""
        This name refers to view that should be the view used by
        default (if no view name is supplied explicitly).""",
        required=False
        )

    cors_origin = TextLine(
        title=u"The name of the view that should be the default." +
              u"[get|post|put|delete]",
        description=u"""
        This name refers to view that should be the view used by
        default (if no view name is supplied explicitly).""",
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
        accept,
        factory,
        for_,
        layer=IDefaultBrowserLayer,
        name=u'',
        cors_enabled=False,
        cors_origin=None,
        permission=CheckerPublic
        ):

    required = {}

    if permission == 'zope.Public':
        permission = CheckerPublic

    for n in ('browserDefault', '__call__', 'publishTraverse'):
        required[n] = permission

    # defineChecker(factory, Checker(required))

    media_types = parse_accept_header(accept)
    for media_type in media_types:
        service_id = register_service(method.upper(), media_type)
        view_name = service_id + name

        adapter(
            _context,
            factory=(factory,),
            provides=IBrowserPublisher,
            for_=(for_, layer),
            name=view_name,
        )

        if cors_enabled:
            # Check if there is already an adapter for options

            service_id = register_service(u'OPTIONS', media_type)
            view_name = u'{}_{}'.format(service_id, name)
            # Register
            adapter(
                _context,
                factory=(get_cors_preflight_view),
                provides=IBrowserPublisher,
                for_=(for_, layer),
                name=view_name,
            )

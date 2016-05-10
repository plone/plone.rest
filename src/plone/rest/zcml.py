# -*- coding: utf-8 -*-
from AccessControl.class_init import InitializeClass
from AccessControl.security import getSecurityInfo
from AccessControl.security import protectClass
from Products.Five.browser import BrowserView
from Products.Five.metaclass import makeClass
from plone.rest.negotiation import parse_accept_header
from plone.rest.negotiation import register_service
from zope.browserpage.metaconfigure import _handle_for
from zope.component.zcml import handler
from zope.configuration.fields import GlobalInterface
from zope.configuration.fields import GlobalObject
from zope.interface import Interface
from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from zope.schema import TextLine
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

    permission = Permission(
        title=u"Permission",
        description=u"The permission needed to access the service.",
        required=True,
        )


def serviceDirective(
        _context,
        method,
        accept,
        factory,
        for_,
        permission,
        layer=IDefaultBrowserLayer,
        name=u'',
        ):

    _handle_for(_context, for_)

    media_types = parse_accept_header(accept)
    for media_type in media_types:
        service_id = register_service(method.upper(), media_type)
        view_name = service_id + name

        # Create a new class. We'll execute some security declarations on it
        # and don't want to modify the original class.
        cdict = getSecurityInfo(factory)
        cdict['__name__'] = view_name
        new_class = makeClass(factory.__name__, (factory, BrowserView), cdict)

        _context.action(
            discriminator=('plone.rest:service', method, media_type, for_,
                           name, layer),
            callable=handler,
            args=('registerAdapter', new_class, (for_, layer), Interface,
                  view_name, _context.info),
        )

        _context.action(
            discriminator=('plone.rest:protectClass', new_class),
            callable=protectClass,
            args=(new_class, permission)
        )
        _context.action(
            discriminator=('plone.rest:InitializeClass', new_class),
            callable=InitializeClass,
            args=(new_class,)
            )

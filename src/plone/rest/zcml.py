# -*- coding: utf-8 -*-
from AccessControl.class_init import InitializeClass
from AccessControl.security import getSecurityInfo
from AccessControl.security import protectClass
from Products.Five.browser import BrowserView
from Products.Five.metaclass import makeClass
from plone.rest.cors import CORSPolicy
from plone.rest.cors import register_method_for_preflight
from plone.rest.interfaces import ICORSPolicy
from plone.rest.negotiation import parse_accept_header
from plone.rest.negotiation import register_service
from zope.browserpage.metaconfigure import _handle_for
from zope.component.zcml import handler
from zope.configuration.fields import GlobalInterface
from zope.configuration.fields import GlobalObject
from zope.interface import Interface
from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from zope.schema import Bool
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

        # We need a service for CORS preflight processing but we don't get the
        # desired Accept header in the preflight request. Thus we just register
        # the current service_id for the given method.
        register_method_for_preflight(method.upper(), service_id)

        # Create a new class. We'll execute some security declarations on it
        # and don't want to modify the original class.
        cdict = getSecurityInfo(factory)
        cdict['__name__'] = view_name
        cdict['method'] = method.upper()
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


class ICORSPolicyDirective(Interface):
    """Directive for defining CORS policies"""

    for_ = GlobalObject(
        title=u"The interface this CORS policy is for.",
        description=u"""Specifies the interface for which the CORS policy is
        registered. If this attribute is not specified, the CORS policy applies
        to all objects.""",
        required=False,
        )

    layer = GlobalInterface(
        title=u"The browser layer for which this CORS policy is registered.",
        description=u"""Useful for overriding existing policies or for making
                        them available only if a specific add-on has been
                        installed.""",
        required=False,
        default=IDefaultBrowserLayer,
        )

    allow_origin = TextLine(
        title=u"Origins",
        description=u"""Origins that are allowed access to the resource. Either
        a comma separated list of origins, e.g. "http://example.net,
        http://mydomain.com" or "*".""",
        )

    allow_methods = TextLine(
        title=u"Methods",
        description=u"""A comma separated list of HTTP method names that are
        allowed by this CORS policy, e.g. "DELETE,GET,OPTIONS,PATCH,POST,PUT".
        """,
        required=False,
        )

    allow_headers = TextLine(
        title=u"Headers",
        description=u"""A comma separated list of request headers allowed to be
        sent by the client, e.g. "X-My-Header".""",
        required=False,
        )

    expose_headers = TextLine(
        title=u"Exposed Headers",
        description=u"""A comma separated list of response headers clients can
        access, e.g. "Content-Length,X-My-Header".""",
        required=False,
        )

    allow_credentials = Bool(
        title=u"Support Credentials",
        description=u"""Indicates whether the resource supports user
        credentials in the request.""",
        default=False,
        )

    max_age = TextLine(
        title=u"Max Age",
        description=u"""Indicates how long the results of a preflight request
        can be cached.""",
        required=False,
        )


def cors_policy_directive(
        _context,
        allow_origin,
        allow_credentials,
        allow_methods=None,
        expose_headers=None,
        allow_headers=None,
        max_age=None,
        for_=Interface,
        layer=IDefaultBrowserLayer,):

    _handle_for(_context, for_)

    # Create a new policy class and store the CORS policy configuration in
    # class attributes.
    cdict = {}
    cdict['allow_origin'] = [o.strip() for o in allow_origin.split(',')]
    if allow_methods is not None:
        cdict['allow_methods'] = [m.strip() for m in allow_methods.split(',')]
    else:
        cdict['allow_methods'] = None
    cdict['allow_credentials'] = allow_credentials
    if expose_headers:
        cdict['expose_headers'] = [
            h.strip() for h in expose_headers.split(',')]
    else:
        cdict['expose_headers'] = []
    if allow_headers:
        cdict['allow_headers'] = [h.strip() for h in allow_headers.split(',')]
    else:
        cdict['allow_headers'] = []
    cdict['max_age'] = max_age
    new_class = makeClass(CORSPolicy.__name__, (CORSPolicy,), cdict)

    _context.action(
        discriminator=('plone.rest:CORSPolicy', for_, layer),
        callable=handler,
        args=('registerAdapter', new_class, (for_, layer),
              ICORSPolicy, u'', _context.info),
        )

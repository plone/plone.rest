from zope import component
from zope.component.interface import provideInterface
from zope.component.zcml import handler
from zope.configuration.fields import GlobalObject, GlobalInterface
from zope.interface import Interface
from zope.publisher.interfaces import IDefaultViewName
from zope.publisher.interfaces.browser import IBrowserRequest
from zope.publisher.interfaces.browser import IBrowserSkinType
from zope.publisher.interfaces.browser import IDefaultSkin
from zope.schema import TextLine, Bool
from zope.publisher.interfaces.browser import IBrowserPublisher
from plone.rest import interfaces

from zope.component.zcml import adapter
from zope.component.zcml import utility


class IService(Interface):
    """
    """

    method = TextLine(
        title=u"The name of the view that should be the default.[get|post|put|delete]",
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
        title=u"The factory for this behavior",
        description=u"If this is not given, the behavior is assumed to provide a marker interface")


    layer = GlobalInterface(
        title=u"A marker interface to be applied by the behavior",
        description=u"If provides is given and factory is not given, then this is optional",
        required=False)

    cors_enabled = Bool(
        title=u"The name of the view that should be the default.[get|post|put|delete]",
        description=u"""
        This name refers to view that should be the view used by
        default (if no view name is supplied explicitly).""",
        required=False
        )

    cors_origin = TextLine(
        title=u"The name of the view that should be the default.[get|post|put|delete]",
        description=u"""
        This name refers to view that should be the view used by
        default (if no view name is supplied explicitly).""",
        required=False
        )

def serviceDirective(_context, method, factory, for_, layer=None, cors_enabled=False, cors_origin=None):
    
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
    else:
        raise ConfigurationError(u"No implementation for %s method" % method)

    # Instantiate the real factory if it's the schema-aware type. We do
    # this here so that the for_ interface may take this into account.
    # if factory is not None and ISchemaAwareFactory.providedBy(factory):
    #     factory = factory(provides)
    
    # registration = ServiceRegistration(
    #     title=title,
    #     description=description,
    #     interface=provides,
    #     marker=marker,
    #     factory=factory)

    # adapter_factory = ServiceAdapterFactory(registration)
    
    adapter(_context, 
            factory=(factory,),
            provides=IBrowserPublisher,
            for_=(for_,marker))
# -*- coding: utf-8 -*-
from plone.rest.interfaces import ICORSPolicy
from plone.rest.interfaces import IService
from zope.component import queryMultiAdapter
from zope.interface import implementer


@implementer(IService)
class Service(object):
    def __call__(self):
        policy = queryMultiAdapter((self.context, self.request), ICORSPolicy)
        if policy is not None:
            if self.request._rest_cors_preflight:
                policy.process_preflight_request()
                return
            else:
                policy.process_simple_request()
        else:
            if self.request._rest_cors_preflight:
                return

        return self.render()

    def render(self):
        raise NotImplementedError

    def __getattribute__(self, name):
        # Preflight requests need to be publicly accessible since they don't
        # include credentials
        if name == "__roles__" and self.request._rest_cors_preflight:
            return ["Anonymous"]
        return super(Service, self).__getattribute__(name)

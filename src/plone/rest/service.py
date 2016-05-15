# -*- coding: utf-8 -*-
from plone.rest.interfaces import ICORSPolicy
from plone.rest.interfaces import IService
from zope.component import queryMultiAdapter
from zope.interface import implements

import json


class Service(object):
    implements(IService)

    def __call__(self):
        policy = queryMultiAdapter((self.context, self.request), ICORSPolicy)
        if policy is not None:
            if self.request._rest_cors_preflight:
                policy.process_preflight_request()
                return
            else:
                policy.process_simple_request()

        self.request.response.setHeader("Content-Type", "application/json")
        return json.dumps(self.render(), indent=2, sort_keys=True)

# -*- coding: utf-8 -*-
from plone.rest.interfaces import IService
from zope.interface import implements

import json


class Service(object):
    implements(IService)

    def __call__(self):
        self.request.response.setHeader("Content-Type", "application/json")
        return json.dumps(self.render(), indent=2, sort_keys=True)

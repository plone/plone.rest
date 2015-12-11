# -*- coding: utf-8 -*-
from Products.Five import BrowserView
from ZPublisher.BaseRequest import DefaultPublishTraverse
from ZPublisher.Iterators import filestream_iterator

import json


class Service(DefaultPublishTraverse, BrowserView):

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def browserDefault(self, request):
        return self, None

    def publishTraverse(self, request, name):
        return super(Service, self).publishTraverse(request, name)

    def __call__(self):
        self.request.response.setHeader("Content-Type", "application/json")
        result = self.render()
        if isinstance(result, filestream_iterator):
            return result
        return json.dumps(result,indent=2, sort_keys=True)

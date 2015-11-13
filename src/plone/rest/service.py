# -*- coding: utf-8 -*-
from ZPublisher.BaseRequest import DefaultPublishTraverse

import json


def json_renderer(func):

    def decorator(*args, **kwargs):
        instance = args[0]
        request = getattr(instance, 'request', None)
        request.response.setHeader(
            'Content-Type',
            'application/json; charset=utf-8'
        )
        result = func(*args, **kwargs)
        return json.dumps(result, indent=2, sort_keys=True)

    return decorator


class Service(DefaultPublishTraverse):

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def browserDefault(self, request):
        return self, None

    def publishTraverse(self, request, name):
        return super(Service, self).publishTraverse(request, name)

    def __call__(self):
        return self.render()

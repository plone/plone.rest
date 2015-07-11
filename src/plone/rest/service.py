import json


class Service(object):

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def browserDefault(self, request):
        return self, None

    def publishTraverse(self, request, name):
        return self

    def __call__(self):
        self.request.response.setHeader("Content-type", "application/json")
        return json.dumps(self.render(), indent=2, sort_keys=True)

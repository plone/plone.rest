# -*- coding: utf-8 -*-
from Products.Five import BrowserView

import json


class Service(BrowserView):

    def __call__(self):
        self.request.response.setHeader("Content-Type", "application/json")
        return json.dumps(self.render(), indent=2, sort_keys=True)

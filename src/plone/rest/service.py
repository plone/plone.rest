# -*- coding: utf-8 -*-
import zope.publisher.browser

import json


class Service(zope.publisher.browser.BrowserPage):

    def __call__(self):
        self.request.response.setHeader("Content-Type", "application/json")
        return json.dumps(self.render(), indent=2, sort_keys=True)

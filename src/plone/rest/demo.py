# -*- coding: utf-8 -*-
from plone.rest import Service
from plone.rest import json_renderer
from zope.component.hooks import getSite


class Get(Service):

    @json_renderer
    def render(self):
        portal = getSite()
        return {'portal_id': portal.id}


class Post(Service):

    @json_renderer
    def render(self):
        return {'service': 'post'}


class Put(Service):

    @json_renderer
    def render(self):
        return {'service': 'put'}


class Delete(Service):

    @json_renderer
    def render(self):
        return {'service': 'delete'}


class Patch(Service):

    @json_renderer
    def render(self):
        return {'service': 'patch'}


class Options(Service):

    @json_renderer
    def render(self):
        return {'service': 'options'}

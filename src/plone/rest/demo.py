# -*- coding: utf-8 -*-

from plone.rest import Service
from zope.component.hooks import getSite


class Get(Service):

    def render(self):
        portal = getSite()
        return {'portal_id': portal.id}


class Post(Service):

    def render(self):
        return {'service': 'post'}


class Put(Service):

    def render(self):
        return {'service': 'put'}


class Delete(Service):

    def render(self):
        return {'service': 'delete'}


class Patch(Service):

    def render(self):
        return {'service': 'patch'}


class Options(Service):

    def render(self):
        return {'service': 'options'}


class NamedGet(Service):

    def render(self):
        return {'service': 'named get'}


class NamedPost(Service):

    def render(self):
        return {'service': 'named post'}


class NamedPut(Service):

    def render(self):
        return {'service': 'named put'}


class NamedDelete(Service):

    def render(self):
        return {'service': 'named delete'}


class NamedPatch(Service):

    def render(self):
        return {'service': 'named patch'}


class NamedOptions(Service):

    def render(self):
        return {'service': 'named options'}

class FilestreamIterator(Service):

    def render(self):
        import os
        from ZPublisher.Iterators import filestream_iterator
        self.request.response.setHeader('content-type', 'application/octet-stream')
        self.request.response.setHeader('content-length', os.path.getsize(__file__))
        return filestream_iterator(os.path.join(
            os.path.dirname(__file__), 'demo.py'))

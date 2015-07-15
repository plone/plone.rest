# -*- coding: utf-8 -*-
from plone.rest import Service


class Get(Service):

    def render(self):
        return {'service': 'get'}


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

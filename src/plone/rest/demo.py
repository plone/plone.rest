# -*- coding: utf-8 -*-
from plone.rest import Service


class Get(Service):

    def render(self):
        return {
            'method': 'GET',
            'id': self.context.id
        }


class Post(Service):

    def render(self):
        return {
            'method': 'POST',
            'id': self.context.id
        }


class Put(Service):

    def render(self):
        return {
            'method': 'PUT',
            'id': self.context.id
        }


class Delete(Service):

    def render(self):
        return {
            'method': 'DELETE',
            'id': self.context.id
        }


class Patch(Service):

    def render(self):
        return {
            'method': 'PATCH',
            'id': self.context.id
        }


class Options(Service):

    def render(self):
        return {
            'method': 'OPTIONS',
            'id': self.context.id
        }


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

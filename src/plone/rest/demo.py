from plone.rest.service import Service


class Demo(Service):

    def render(self):
        return {'demo': 'demo'}

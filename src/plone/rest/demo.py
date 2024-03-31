from plone.rest import Service

import json


class BaseService(Service):
    def render(self):
        self.request.response.setHeader("Content-Type", "application/json")
        return json.dumps(self.data(), indent=2, sort_keys=True)


class Get(BaseService):
    def data(self):
        if self.request.form and self.request.form.get("query"):
            # the query parameter is a json-encoded query string and needs to be parsed as json
            self.request.form["query"] = json.loads(self.request.form.get("query"))
            return {"method": "GET", "id": self.context.id, "body": self.request.form}
        return {"method": "GET", "id": self.context.id}


class Post(BaseService):
    def data(self):
        return {"method": "POST", "id": self.context.id}


class Put(BaseService):
    def data(self):
        return {"method": "PUT", "id": self.context.id}


class Delete(BaseService):
    def data(self):
        return {"method": "DELETE", "id": self.context.id}


class Patch(BaseService):
    def data(self):
        return {"method": "PATCH", "id": self.context.id}


class Options(BaseService):
    def data(self):
        return {"method": "OPTIONS", "id": self.context.id}


class NamedGet(BaseService):
    def data(self):
        return {"service": "named get"}


class NamedPost(BaseService):
    def data(self):
        return {"service": "named post"}


class NamedPut(BaseService):
    def data(self):
        return {"service": "named put"}


class NamedDelete(BaseService):
    def data(self):
        return {"service": "named delete"}


class NamedPatch(BaseService):
    def data(self):
        return {"service": "named patch"}


class NamedOptions(BaseService):
    def data(self):
        return {"service": "named options"}

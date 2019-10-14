# -*- coding: utf-8 -*-
from datetime import datetime
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing import SITE_OWNER_NAME
from plone.app.testing import SITE_OWNER_PASSWORD
from plone.app.textfield.value import RichTextValue
from plone.namedfile.file import NamedBlobImage
from plone.namedfile.file import NamedBlobFile
from plone.rest.testing import PLONE_REST_FUNCTIONAL_TESTING
from z3c.relationfield import RelationValue
from zope.component import getUtility
from zope.intid.interfaces import IIntIds

import unittest
import os
import requests
import transaction


class TestDexterityServiceEndpoints(unittest.TestCase):

    layer = PLONE_REST_FUNCTIONAL_TESTING

    def setUp(self):
        self.app = self.layer["app"]
        self.request = self.layer["request"]
        self.portal = self.layer["portal"]
        self.portal_url = self.portal.absolute_url()
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self.portal.invokeFactory("Document", id="doc1")
        self.document = self.portal["doc1"]
        transaction.commit()

    def test_dexterity_document_get(self):
        response = requests.get(
            self.document.absolute_url(),
            headers={"Accept": "application/json"},
            auth=(SITE_OWNER_NAME, SITE_OWNER_PASSWORD),
        )
        self.assertEqual(200, response.status_code)
        self.assertEqual(u"doc1", response.json().get("id"))
        self.assertEqual(u"GET", response.json().get("method"))

    def test_dexterity_document_post(self):
        response = requests.post(
            self.document.absolute_url(),
            headers={"Accept": "application/json"},
            auth=(SITE_OWNER_NAME, SITE_OWNER_PASSWORD),
        )
        self.assertEqual(200, response.status_code)
        self.assertEqual(u"doc1", response.json().get("id"))
        self.assertEqual(u"POST", response.json().get("method"))

    def test_dexterity_document_put(self):
        response = requests.put(
            self.document.absolute_url(),
            headers={"Accept": "application/json"},
            auth=(SITE_OWNER_NAME, SITE_OWNER_PASSWORD),
        )
        self.assertEqual(200, response.status_code)
        self.assertEqual(u"doc1", response.json().get("id"))
        self.assertEqual(u"PUT", response.json().get("method"))

    def test_dexterity_document_patch(self):
        response = requests.patch(
            self.document.absolute_url(),
            headers={"Accept": "application/json"},
            auth=(SITE_OWNER_NAME, SITE_OWNER_PASSWORD),
        )
        self.assertEqual(200, response.status_code)
        self.assertEqual(u"doc1", response.json().get("id"))
        self.assertEqual(u"PATCH", response.json().get("method"))

    def test_dexterity_document_delete(self):
        response = requests.delete(
            self.document.absolute_url(),
            headers={"Accept": "application/json"},
            auth=(SITE_OWNER_NAME, SITE_OWNER_PASSWORD),
        )
        self.assertEqual(200, response.status_code)
        self.assertEqual(u"doc1", response.json().get("id"))
        self.assertEqual(u"DELETE", response.json().get("method"))

    def test_dexterity_document_options(self):
        response = requests.options(
            self.document.absolute_url(),
            headers={"Accept": "application/json"},
            auth=(SITE_OWNER_NAME, SITE_OWNER_PASSWORD),
        )
        self.assertEqual(200, response.status_code)
        self.assertEqual(u"doc1", response.json().get("id"))
        self.assertEqual(u"OPTIONS", response.json().get("method"))

    def test_dexterity_folder_get(self):
        self.portal.invokeFactory("Folder", id="folder")
        transaction.commit()

        response = requests.get(
            self.portal.folder.absolute_url(),
            headers={"Accept": "application/json"},
            auth=(SITE_OWNER_NAME, SITE_OWNER_PASSWORD),
        )

        self.assertEqual(200, response.status_code)
        self.assertEqual(u"folder", response.json().get("id"))
        self.assertEqual(u"GET", response.json().get("method"))

    def test_dexterity_news_item_get(self):
        self.portal.invokeFactory("News Item", id="newsitem")
        self.portal.newsitem.title = "My News Item"
        self.portal.newsitem.description = u"This is a news item"
        self.portal.newsitem.text = RichTextValue(
            u"Lorem ipsum", "text/plain", "text/html"
        )
        image_file = os.path.join(os.path.dirname(__file__), u"image.png")
        fd = open(image_file, "rb")
        self.portal.newsitem.image = NamedBlobImage(
            data=fd.read(), contentType="image/png", filename=u"image.png"
        )
        fd.close()
        self.portal.newsitem.image_caption = u"This is an image caption."
        import transaction

        transaction.commit()
        response = requests.get(
            self.portal.newsitem.absolute_url(),
            headers={"Accept": "application/json"},
            auth=(SITE_OWNER_NAME, SITE_OWNER_PASSWORD),
        )

        self.assertEqual(200, response.status_code)
        self.assertEqual(u"newsitem", response.json().get("id"))
        self.assertEqual(u"GET", response.json().get("method"))

    def test_dexterity_event_get(self):
        self.portal.invokeFactory("Event", id="event")
        self.portal.event.title = "Event"
        self.portal.event.description = u"This is an event"
        self.portal.event.start = datetime(2013, 1, 1, 10, 0)
        self.portal.event.end = datetime(2013, 1, 1, 12, 0)
        import transaction

        transaction.commit()
        response = requests.get(
            self.portal.event.absolute_url(),
            headers={"Accept": "application/json"},
            auth=(SITE_OWNER_NAME, SITE_OWNER_PASSWORD),
        )

        self.assertEqual(200, response.status_code)
        self.assertEqual(u"event", response.json().get("id"))
        self.assertEqual(u"GET", response.json().get("method"))

    def test_dexterity_link_get(self):
        self.portal.invokeFactory("Link", id="link")
        self.portal.link.title = "My Link"
        self.portal.link.description = u"This is a link"
        self.portal.remoteUrl = "http://plone.org"
        import transaction

        transaction.commit()
        response = requests.get(
            self.portal.link.absolute_url(),
            headers={"Accept": "application/json"},
            auth=(SITE_OWNER_NAME, SITE_OWNER_PASSWORD),
        )

        self.assertEqual(200, response.status_code)
        self.assertEqual(u"link", response.json().get("id"))
        self.assertEqual(u"GET", response.json().get("method"))

    def test_dexterity_file_get(self):
        self.portal.invokeFactory("File", id="file")
        self.portal.file.title = "My File"
        self.portal.file.description = u"This is a file"
        pdf_file = os.path.join(os.path.dirname(__file__), u"file.pdf")
        fd = open(pdf_file, "rb")
        self.portal.file.file = NamedBlobFile(
            data=fd.read(), contentType="application/pdf", filename=u"file.pdf"
        )
        fd.close()
        intids = getUtility(IIntIds)
        file_id = intids.getId(self.portal.file)
        self.portal.file.file = RelationValue(file_id)
        import transaction

        transaction.commit()

        response = requests.get(
            self.portal.file.absolute_url(),
            headers={"Accept": "application/json"},
            auth=(SITE_OWNER_NAME, SITE_OWNER_PASSWORD),
        )

        self.assertEqual(200, response.status_code)
        self.assertEqual(u"file", response.json().get("id"))
        self.assertEqual(u"GET", response.json().get("method"))

    def test_dexterity_image_get(self):
        self.portal.invokeFactory("Image", id="image")
        self.portal.image.title = "My Image"
        self.portal.image.description = u"This is an image"
        image_file = os.path.join(os.path.dirname(__file__), u"image.png")
        fd = open(image_file, "rb")
        self.portal.image.image = NamedBlobImage(
            data=fd.read(), contentType="image/png", filename=u"image.png"
        )
        fd.close()
        import transaction

        transaction.commit()

        response = requests.get(
            self.portal.image.absolute_url(),
            headers={"Accept": "application/json"},
            auth=(SITE_OWNER_NAME, SITE_OWNER_PASSWORD),
        )

        self.assertEqual(200, response.status_code)
        self.assertEqual(u"image", response.json().get("id"))
        self.assertEqual(u"GET", response.json().get("method"))

    def test_dexterity_collection_get(self):
        self.portal.invokeFactory("Collection", id="collection")
        self.portal.collection.title = "My Collection"
        self.portal.collection.description = u"This is a collection with two documents"
        self.portal.collection.query = [
            {
                "i": "portal_type",
                "o": "plone.app.querystring.operation.string.is",
                "v": "Document",
            }
        ]
        self.portal.invokeFactory("Document", id="doc2", title="Document 2")
        import transaction

        transaction.commit()
        response = requests.get(
            self.portal.collection.absolute_url(),
            headers={"Accept": "application/json"},
            auth=(SITE_OWNER_NAME, SITE_OWNER_PASSWORD),
        )

        self.assertEqual(200, response.status_code)
        self.assertEqual(u"collection", response.json().get("id"))
        self.assertEqual(u"GET", response.json().get("method"))

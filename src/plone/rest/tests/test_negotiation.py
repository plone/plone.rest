# -*- coding: utf-8 -*-
from plone.rest.negotiation import lookup_service_id
from plone.rest.negotiation import parse_accept_header
from plone.rest.negotiation import register_service

import unittest


class TestAcceptHeaderParser(unittest.TestCase):

    def test_parse_application_json_accept_header(self):
        accept = 'application/json'
        expected = [('application', 'json')]
        self.assertEqual(expected, parse_accept_header(accept))

    def test_parse_jquery_json_accept_header(self):
        accept = ('text/javascript, application/javascript, '
                  'application/ecmascript, application/x-ecmascript, '
                  '*/*; q=0.01')
        expected = [('text', 'javascript'),
                    ('application', 'javascript'),
                    ('application', 'ecmascript'),
                    ('application', 'x-ecmascript'),
                    ('*', '*')]
        self.assertEqual(expected, parse_accept_header(accept))

    def test_parse_firefox_accept_header(self):
        accept = ('text/html,application/xhtml+xml,application/xml;q=0.9,'
                  '*/*;q=0.8')
        expected = [('text', 'html'),
                    ('application', 'xhtml+xml'),
                    ('application', 'xml'),
                    ('*', '*')]
        self.assertEqual(expected, parse_accept_header(accept))

    def test_parse_chrome_accept_header(self):
        accept = ('text/html,application/xhtml+xml,application/xml;q=0.9,'
                  'image/webp,*/*;q=0.8')
        expected = [('text', 'html'),
                    ('application', 'xhtml+xml'),
                    ('application', 'xml'),
                    ('image', 'webp'),
                    ('*', '*')]
        self.assertEqual(expected, parse_accept_header(accept))

    def test_parse_all_media_types_accept_header(self):
        self.assertEqual([('*', '*')], parse_accept_header('*/*'))

    def test_parse_invalid_accept_header(self):
        self.assertEqual([], parse_accept_header('invalid'))


class TestServiceRegistry(unittest.TestCase):

    def test_register_media_type(self):
        self.assertEqual(u'GET_application_json_',
                         register_service('GET', ('application', 'json')))
        self.assertEqual(u'GET_application_json_',
                         lookup_service_id('GET', 'application/json'))

    def test_register_wildcard_subtype(self):
        self.assertEqual(u'PATCH_text_*_',
                         register_service('PATCH', ('text', '*')))
        self.assertEqual(u'PATCH_text_*_',
                         lookup_service_id('PATCH', 'text/xml'))

    def test_register_wilcard_type(self):
        self.assertEqual(u'PATCH_*_*_', register_service('PATCH', ('*', '*')))
        self.assertEqual(u'PATCH_*_*_', lookup_service_id('PATCH', 'foo/bar'))

    def test_service_id_for_multiple_media_types_is_none(self):
        register_service('GET', 'application/json')
        self.assertEqual(None, lookup_service_id(
            'GET', 'application/json,application/javascipt'))

    def test_service_id_for_invalid_media_type_is_none(self):
        self.assertEqual(None, lookup_service_id('GET', 'application-json'))

    def test_service_id_for_not_registered_media_type_is_none(self):
        self.assertEqual(None, lookup_service_id('PUT', 'text/html'))

    def test_service_id_for_wildcard_type_is_none(self):
        register_service('GET', 'application/json')
        self.assertEqual(None, lookup_service_id('GET', '*/*'))

    def test_service_id_for_wildcard_subtype_is_none(self):
        register_service('GET', 'text/xml')
        self.assertEqual(None, lookup_service_id('GET', 'text/*'))

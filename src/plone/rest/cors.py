# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.
import fnmatch
import functools
from plone.rest.service import Service


class Options(Service):

    def render(self):
        return None


def preflight(request, cors_config_dict):
    response = request.response
    origin = request.getHeader('Origin', None)
    if not origin:
        request.response.setStatus(404, 'Origin this header is mandatory')
    requested_method = request.getHeader('Access-Control-Request-Method', None)
    if not requested_method:
        request.response.setStatus(404, 'Access-Control-Request-Method' +
                                        'this header is mandatory')

    if not (requested_method and origin):
        return

    requested_headers = (
        request.getHeader('Access-Control-Request-Headers', ()))

    if requested_headers:
        requested_headers = map(str.strip, requested_headers.split(', '))

    requested_method = requested_method.upper()
    if requested_method not in cors_config_dict.keys():
        request.response.setStatus(404, 'Access-Control-Request-Method' +
                                        'Method not allowed')

    supported_headers = cors_config_dict[requested_method]['headers']
    if not cors_config_dict[requested_method]['expose_all_headers'] and requested_headers and supported_headers:
        for h in requested_headers:
            if not h.lower() in [s.lower() for s in supported_headers]:
                request.response.setStatus(
                    404,
                    'Access-Control-Request-Headers' +
                    'Header "%s" not allowed' % h)

    supported_headers = [] if supported_headers is None else supported_headers
    requested_headers = [] if requested_headers is None else requested_headers

    supported_headers = set(supported_headers) | set(requested_headers)

    response.setHeader(
        'Access-Control-Allow-Headers',
        ','.join(supported_headers))

    response.setHeader(
        'Access-Control-Allow-Methods',
        ','.join(cors_config_dict.keys()))

    max_age = cors_config_dict[requested_method]['max_age']
    if max_age is not None:
        response.setHeader('Access-Control-Max-Age', str(max_age))

    return None


def options_view_wrap(fn, cors_config_dict, cors_config):
    def function_wrapped(context, request):
        apply_cors_post_request(cors_config, request, request.response)
        result = fn(context, request)
        preflight(request, cors_config_dict)
        return result
    return function_wrapped


def options_view(cors_config_dict):

    def function_wrapped(context, request):
        preflight(request, cors_config_dict)
        return Options(context, request)

    return function_wrapped


def wrap_cors(fn, cors_config):
    def function_wrapped(context, request):
        result = fn(context, request)
        apply_cors_post_request(cors_config, request, request.response)
        return result

    return function_wrapped


def ensure_origin(cors_config, request, response=None):
    """Ensure that the origin header is set and allowed."""
    response = response or request.response

    # Don't check this twice.
    if not hasattr(request, '_v_cors_checked'):

        origin = request.getHeader('Origin')
        if origin:
            if not any([fnmatch.fnmatchcase(origin, o)
                        for o in cors_config['origin']]):
                request.response.setStatus(404, 'Origin %s not allowed' % origin)
            elif request.getHeader(
                    'Access-Control-Allow-Credentials', False):
                response.setHeaders('Access-Control-Allow-Origin', origin)
            else:
                if any([o == "*" for o in cors_config['origin']]):
                    response.setHeader('Access-Control-Allow-Origin', '*')
                else:
                    response.setHeaders('Access-Control-Allow-Origin', origin)
        request._v_cors_checked = True
    return response


def get_cors_validator(service):
    return functools.partial(ensure_origin, service)


def apply_cors_post_request(cors_config, request, response):
    """Handles CORS-related post-request things.

    Add some response headers, such as the Expose-Headers and the
    Allow-Credentials ones.
    """
    response = ensure_origin(cors_config, request, response)

    # TODO Support Allow Credentials
    # if (service.cors_support_credentials_for(method) and
    #         'Access-Control-Allow-Credentials' not in response.headers):
    #     response.headers['Access-Control-Allow-Credentials'] = 'true'

    if request.method != 'OPTIONS':
        # Which headers are exposed?
        supported_headers = cors_config['headers']
        if supported_headers:
            response.setHeader(
                'Access-Control-Expose-Headers',
                ', '.join(supported_headers))

    return response

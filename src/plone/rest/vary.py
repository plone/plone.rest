# -*- coding: utf-8 -*-
def add_vary_accept_header(event):
    """Add the ``Vary: Accept`` header for all responses """

    response = event.request.RESPONSE
    response.addHeader('Vary', 'Accept')

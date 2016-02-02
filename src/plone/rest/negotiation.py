# -*- coding: utf-8 -*-

# Service registry
# A mapping of method -> type name -> subtype name -> service id
_services = {}


def parse_accept_header(accept):
    """Parse the given Accept header ignoring any parameters and return a list
       of media type tuples.
    """
    media_types = []
    for media_range in accept.split(','):
        media_type = media_range.split(';')[0].strip()
        if '/' in media_type:
            type_, subtype = media_type.split('/')
            media_types.append((type_, subtype))
    return media_types


def lookup_service_id(method, accept):
    """Lookup the service id for the given request method and Accept header.
       Only Accept headers containing exactly one media type are considered for
       negotiation.
    """
    media_types = parse_accept_header(accept)
    if len(media_types) != 1:
        return None
    type_, subtype = media_types[0]
    types = _services.get(method, {})
    subtypes = types.get(type_, {})
    if subtype in subtypes:
        return subtypes[subtype]
    elif '*' in subtypes:
        return subtypes['*']
    if '*' in types:
        return types['*']['*']
    return None


def register_service(method, media_type):
    """Register a service for the given request method and media type and
       return it's service id.
    """
    service_id = u'{}_{}_{}_'.format(method, media_type[0], media_type[1])
    types = _services.setdefault(method, {})
    subtypes = types.setdefault(media_type[0], {})
    subtypes[media_type[1]] = service_id
    return service_id

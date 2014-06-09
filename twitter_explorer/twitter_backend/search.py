"""Twitter search related utilities."""

import urllib


def _parse_search(search_results):
    """Parse search results and return a list of dicts. Each dict has the
    following se of fileds:
        - text
        - author
        - geo_data
    """
    if not search_results:
        return []

    return [
        {
            'text': t.text,
            'author': t.author.screen_name,
            'geo_data': get_map_for_geo(t.geo.get('coordinates'))
                        if t.geo else None
        }
        for t in search_results]



def search(api, query, count=50):
    """Search for tweets and return parsed data."""
    return _parse_search(api.search(query, count=count))


def get_map_for_geo(coordinates):
    """Return a Google Map URL for the given coordinates."""
    params = {
        'q': ','.join(str(p) for p in coordinates)
    }
    url = 'http://google.com/search?%s' % (urllib.urlencode(params))
    print url
    return url

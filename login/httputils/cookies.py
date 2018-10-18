import urllib2

__doc__ = """simple cookie extraction"""

def extract_cookie(response):
    """"extract cookie from a response"""
    return response.info().get("set-cookie", None)

def get_cookie(resource, *args, **kwargs):
    """make a request and extract the cookie"""
    return extract_cookies(urllib2.urlopen(resource, *args, **kwargs))

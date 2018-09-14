import copy
import HTMLParser
import os
import re
import sys
import urllib2

sys.path.append(os.path.realpath(__file__))

import uri

__doc__ = """HTML forms"""

def generate_forms(html):
    """generate HTMLForm instances from an HTML document"""
    parser = HTMLFormParser()
    parser.feed(html)
    ##############################generate forms
    parser.close()

class HTMLForm:
    def __init__(self, action, method = "get", inputs = {}):
        self.action = action
        self.inputs = inputs
        self.method = method

    def make(self):
        method = self.method.lower()
        
        if method == "get":
            url = uri.URL(self.action)
            url.query = uri.Query(self.inputs)
            return urllib2.Request(str(url))
        elif method == "post":
            return urllib2.Request(self.action, str(uri.Query(self.inputs)))
        raise ValueError("no such submission method: %s" % self.method)
    
    def submit(self):
        pass

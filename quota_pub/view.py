import web
import re
import json
import operator
import math

from time import time
from __version__ import version

CACHE = False
TEMPLATES = 'templates/'

render = web.template.render(cache=CACHE)
#render._keywords['globals']['render'] = render

class index:
    def GET(self, size):
        return render.base(view_index(size))

class tenant:
    def GET(self, name):
        #web.header('Content-Type', 'application/json')
        return view_tenant(name)
    
class alltenants:
    def GET(self, count):
        web.header('Content-Type', 'application/json')
        return view_alltenants()

def view_index(size):
    """
        returns an index template
    """
    return render.index(time(), 1, 1, 1, 1, 0)

def view_tenant(name):
    """
        returns the specified tenant target value
    """
    print name
    tenants = web.tenants
    if tenants:
        if name in tenants.keys():
            return tenants[name]
        else: 
            return "Not Found"
    return None


def view_alltenants():
    """
        returns the all tenants as a JSON formatted str
    """
    tenants = web.tenants
    if tenants:
        return json.dumps(tenants)
    else:
        return json.dumps(None)


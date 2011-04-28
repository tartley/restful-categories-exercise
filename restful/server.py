
from urllib2 import HTTPError

import web

from .api import add_category, get_category, get_subcategories


urls = (
    '/', 'Children',
    '/category/(.*)', 'Category',
    '/children/(.*)', 'Children',
    #'/lineage/(.*)',
)


# note: I duplicated the POST hander for Children and Category, so that
# Children can handle 'POST /' requests, to create new top-level categories,
# and Category can handle 'POST /category/ID' to create new subcategories.
# A better solution might be a redirect

class Children(object):
    """
    handler of requests for the children of a given category
    """
    def GET(self, cat_id=None):
        return get_subcategories(cat_id)

    def POST(self, parent_id=None):
        category_name = web.input().name
        return add_category(category_name, parent_id)


class Category(object):

    def GET(self, cat_id):
        return get_category(cat_id)


def main():
    app = web.application(urls, globals())
    app.run()


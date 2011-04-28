
import json
from urllib2 import HTTPError

import web

from .api import add_category, get_category, get_subcategories
from .representation import category_info, category_detail


urls = (
    '/', 'Children',
    '/category/(.*)', 'Category',
    '/children/(.*)', 'Children',
    #'/lineage/(.*)',
)


class Children(object):
    """
    handler of requests for the children of a given category
    """
    def GET(self, cat_id=None):
        return json.dumps( get_subcategories(cat_id) )

    def POST(self, parent_id=None):
        cat_name = web.input().name
        return (
            json.dumps(
                category_info(
                    add_category(cat_name, parent_id)
                )
            )
        )


class Category(object):

    def GET(self, cat_id):
        return get_category(cat_id)

    #def PUT(self, category):
        # create new category
        # request looks like:
        #   PUT http://server/category/NAME
        #   { parent_id: ID }
        #pass


def main():
    app = web.application(urls, globals())
    app.run()


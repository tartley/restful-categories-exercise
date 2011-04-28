
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



def _make_int(cat_id):
    if cat_id is not None:
        try:
            return int(cat_id)
        except ValueError:
            # I'd like to raise web.badrequest() here, but it doesn't
            # return a 400 status like I'd expect.
            raise


class Children(object):
    """
    handler of requests for the children of a given category
    """
    def GET(self, cat_id=None):
        cat_id = _make_int(cat_id)
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
        cat_id = _make_int(cat_id)
        return json.dumps( category_detail( get_category(cat_id) ) )

    #def PUT(self, category):
        # create new category
        # request looks like:
        #   PUT http://server/category/NAME
        #   { parent_id: ID }
        #pass


def main():
    app = web.application(urls, globals())
    app.run()


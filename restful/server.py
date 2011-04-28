
import json
from urllib2 import HTTPError

import web

from .api import get_subcategories


urls = (
    '/', 'Children',
    #'/category/(.*)', 'Category',
    '/children/(.*)', 'Children',
    #'/lineage/(.*)',
)



class Children(object):
    """
    handler of requests for the children of a given category
    """
    def GET(self, catid=None):
        if catid is not None:
            try:
                catid = int(catid)
            except ValueError:
                # I'd like to raise web.badrequest() here, but it doesn't return
                # a 400 error like I'd expect.
                raise

        return get_subcategories(catid)

    #def POST(self, catid):
        #new_category = add_category(web.input().name)
        #raise web.seeother('/category/%s' % (new_category.uid))

#class Category(object):

    #def GET(self, catid):
        #return get_category(catid)
        #return json.dumps( {categories:'/categories/'} )

    #def PUT(self, category):
        # create new category
        # request looks like:
        #   PUT http://server/category/NAME
        #   { parent_id: ID }
        #pass


def main():
    app = web.application(urls, globals())
    app.run()


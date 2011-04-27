
import json

import web

from .api import get_subcategories


urls = (
    #'/',
    #'/category/(.*)', 'Category',
    '/children/(.*)', 'Children',
    #'/lineage/(.*)',
)



class Children(object):

    def GET(self, catid):
        return get_subcategories(int(catid))

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


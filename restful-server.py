
import json
import web


# storage layer (to be replaced by something persistent)

_next_uid = 0

def _get_next_uid():
    global _next_uid
    _next_uid += 1
    return _next_uid

class ModelCategory(object):
    def __init__(self, name, parent=None):
        self.uid = _get_next_uid()
        self.name = name
        self.parent = parent

electronics = ModelCategory('Electronics')
books = ModelCategory('Books')
fiction = ModelCategory('Fiction', books)
nonfiction = ModelCategory('Non-Fiction', books)


all_categories = {}

def add(category):
    all_categories[category.uid] = category

add(electronics)
add(books)
add(fiction)
add(nonfiction)



# supported API

def add_category(name, parent_id=None):
    parent = None
    if parent_id:
        parent = all_categories.get[parent_id]

    new_category = ModelCategory(name, parent)
    all_categories[ new_category.uid ] = new_category
    return new_category

def get_subcategories(category_id):
    print category_id
    category = all_categories.get(category_id, None)
    print category
    if category:
        return [
            child.name
            for child in all_categories.itervalues()
            if child.parent == category
        ]
    else:
        raise Exception('???')

def get_lineage(category_id):
    lineage = []
    category = all_categories[category_id]
    while True:
        if category.parent:
            lineage.append(category.parent)
            category = all_categories[ category.parent.uid ]
        else:
            break
    return lineage



# url mapping

urls = (
    #'/',
    #'/category/(.*)', 'Category',
    '/children/(.*)', 'Children',
    #'/lineage/(.*)',
)
app = web.application(urls, globals())



# handlers

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


if __name__ == "__main__":
    app.run()


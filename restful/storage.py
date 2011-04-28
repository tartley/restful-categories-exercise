
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

all_categories = {}


def add(category):
    all_categories[category.uid] = category



electronics = ModelCategory('Electronics')
books = ModelCategory('Books')
fiction = ModelCategory('Fiction', books)
nonfiction = ModelCategory('Non-Fiction', books)


# When storage layer is replaced with a DB,
# this function will just connect to a test DB instead of the live one
# For now it just populates the DB with some test data
add(electronics)
add(books)
add(fiction)
add(nonfiction)




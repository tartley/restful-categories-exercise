
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


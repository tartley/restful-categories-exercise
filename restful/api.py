
from .storage import all_categories


# supported API

#def add_category(name, parent_id=None):
    #parent = None
    #if parent_id:
        #parent = all_categories.get[parent_id]

    #new_category = ModelCategory(name, parent)
    #all_categories[ new_category.uid ] = new_category
    #return new_category

def get_subcategories(category_id):
    category = all_categories.get(category_id, None)
    if category:
        return [
            child.name
            for child in all_categories.itervalues()
            if child.parent == category
        ]
    else:
        raise Exception('???')

#def get_lineage(category_id):
    #lineage = []
    #category = all_categories[category_id]
    #while True:
        #if category.parent:
            #lineage.append(category.parent)
            #category = all_categories[ category.parent.uid ]
        #else:
            #break
    #return lineage



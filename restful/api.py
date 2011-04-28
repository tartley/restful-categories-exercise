'''
API defined by the spec
'''

import json

import web

from .representation import category_detail, category_info
from .storage import all_categories, ModelCategory



def _make_int(cat_id):
    if cat_id is not None:
        try:
            return int(cat_id)
        except ValueError:
            # I'd like to raise web.badrequest() here, but it doesn't
            # return a 400 status like I'd expect.
            raise



def get_category(category_id):
    return json.dumps(
        category_detail(
            all_categories[_make_int(category_id)]
        )
    )


def get_subcategories(category_id):
    category = all_categories.get(_make_int(category_id), None)
    return [
        category_info(child)
        for child in all_categories.itervalues()
        if child.parent == category
    ]


def add_category(name, parent_id=None):
    parent = None
    if parent_id:
        parent = all_categories[_make_int(parent_id)]

    new_category = ModelCategory(name, parent)
    all_categories[ new_category.uid ] = new_category
    return new_category


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



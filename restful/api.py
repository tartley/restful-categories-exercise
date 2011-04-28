'''
API defined by the spec
'''

import json

import web

from .storage import all_categories, ModelCategory


def add_category(name, parent_id=None):
    parent = None
    if parent_id:
        parent = all_categories.get[parent_id]

    new_category = ModelCategory(name, parent)
    all_categories[ new_category.uid ] = new_category
    return new_category


def _cat_to_dict(category):
    return dict(
        name=category.name,
        uri='%s/category/%d' % (web.ctx.homedomain, category.uid)
    )

def get_subcategories(category_id):
    category = all_categories.get(category_id, None)
    return [
        _cat_to_dict(child)
        for child in all_categories.itervalues()
        if child.parent == category
    ]


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



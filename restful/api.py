'''
API defined by the spec
'''

import json

import web

from .representation import category_detail, category_list
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
    '''
    This API entry point isn't actually required by the spec, I added it
    to facilitate browsing the API, e.g. going from list of subcats, to
    getting details for a particular child (using this function), and then
    adding new subcategories under that child.
    '''
    return json.dumps(
        category_detail(
            all_categories[_make_int(category_id)]
        )
    )


def get_subcategories(category_id):
    '''
    For the given category, returns a list of its immediate children in the
    tree.

    Example, get_subcategories(BOOK_ID) returns the following, as JSON:
    [
        {name='Fiction', uri=FICTION_URI},
        {name='Non-Fiction', uri=NON_FICTION_URI},
    ]
    '''
    category = all_categories.get(_make_int(category_id), None)
    return json.dumps(
        category_list( [
            child
            for child in all_categories.itervalues()
            if child.parent == category
        ] )
    )


def add_category(name, parent_id=None):
    '''
    Adds a new category as a direct child of the given parent category.

    Example: add_category(‘Science Fiction’, FICTION_ID) will add Science
    Fiction as a new subcategory of Fiction.

    If parent is omitted, adds a new top-level category

    Returns the JSON representation of the newly-added category.
    '''
    parent = None
    if parent_id:
        parent = all_categories[_make_int(parent_id)]

    new_category = ModelCategory(name, parent)
    all_categories[ new_category.uid ] = new_category
    return json.dumps(
        category_detail(new_category)
    )


def get_lineage(category_id):
    '''
    For a given category, retrieve a list showing its ancestry within the
    tree. Example: get_lineage(LAPTOPS_ID) returns
    [
        {name='Electronics', uri=ELECTRONICS_URI},
        {name='Computers', uri=COMPUTERS_URI},
        {name='Laptops', uri=LAPTOPS_URI},
    ]
    '''
    lineage = []
    category = all_categories[_make_int(category_id)]
    while True:
        if category.parent:
            lineage.append(category.parent)
            category = all_categories[ category.parent.uid ]
        else:
            break
    return json.dumps(
        category_list(lineage)
    )



import json

import web


def category_uri(category):
    uid = ''
    if category is not None:
        uid = category.uid
    return web.ctx.homedomain + '/category/%s' % (uid,)


def children_uri(category):
    return web.ctx.homedomain + '/children/%d' % (category.uid,)


def lineage_uri(category):
    return web.ctx.homedomain + '/lineage/%d' % (category.uid,)


def category_info(category):
    return dict(
        name=category.name,
        uri=category_uri(category),
    )


def category_detail(category):
    return dict(
        name=category.name,
        parent=category_uri(category.parent),
        children=children_uri(category),
        lineage=lineage_uri(category),
    )


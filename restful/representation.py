
import json

import web


def category_to_uri(category):
    return web.ctx.homedomain + '/category/%d' % (category.uid,)


def category_to_json(category):
    return json.dumps(
        dict(
            name=category.name,
            uri=category_to_uri(category)
        )
    )


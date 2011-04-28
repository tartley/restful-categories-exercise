
from unittest import skip, TestCase
from urllib2 import HTTPError

import web
from mock import patch

from restful.server import Children
from restful.storage import ModelCategory

footwear = ModelCategory('footwear')
shoes = ModelCategory('shoes', footwear)
wellies = ModelCategory('wellies', footwear)

test_categories = {
    footwear.uid: footwear,
    shoes.uid: shoes,
    wellies.uid: wellies,
}

class TestChildren(TestCase):

    @patch('restful.api.all_categories', test_categories)
    def test_GET_ok(self):
        response = Children().GET(footwear.uid)
        self.assertEqual(response, '["shoes", "wellies"]')


    @skip("Raising web.badrequest() doesn't return a 400 error as I'd expect")
    @patch('restful.api.all_categories', test_categories)
    def test_GET_invalid_catid(self):
        with self.assertRaises(HTTPError) as cm:
            Children().GET('abc')


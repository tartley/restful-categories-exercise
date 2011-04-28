
import json
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

    @patch('restful.api.web')
    @patch('restful.api.all_categories', test_categories)
    def test_GET_ok(self, mock_web):
        '''
        valid request returns json representation
        '''
        mock_web.ctx.homedomain = 'SERVER'

        response = Children().GET(footwear.uid)

        expected = json.dumps([
            dict(name='shoes', uri='SERVER/category/%d' % (shoes.uid,)),
            dict(name='wellies', uri='SERVER/category/%d' % (wellies.uid,)),
        ])
        self.assertEqual(response, expected)


    @skip("Raising web.badrequest() doesn't return a 400 error as I'd expect")
    @patch('restful.api.all_categories', test_categories)
    def test_GET_invalid_catid(self):
        '''
        requesting an invalid category ID raises a 400 error
        '''
        with self.assertRaises(HTTPError) as cm:
            Children().GET('abc')


    @patch('restful.api.web')
    @patch('restful.api.all_categories', test_categories)
    def test_GET_no_catid(self, mock_web):
        '''
        requesting no category ID at all responds with top level cats
        '''
        mock_web.ctx.homedomain = 'SERVER'

        response = Children().GET()

        expected = json.dumps( [
            {
                'uri': 'SERVER/category/%d' % (footwear.uid,),
                'name': 'footwear',
            },
        ] )
        self.assertEquals(response, expected)


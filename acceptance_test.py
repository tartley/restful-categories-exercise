
import json
from subprocess import check_output, Popen, PIPE, STDOUT
from unittest import TestCase, main


BASE_URI = 'http://localhost:8080'
CATEGORY_URI = BASE_URI + '/category/'
CHILDREN_URI = BASE_URI + '/children/'
LINEAGE_URI = BASE_URI + '/lineage/'


class Unknown(object):
    '''
    Equal to everything. Used as a placeholder for values we don't know
    when comparing collections full of values.
    '''
    def __eq__(*_):
        return True

unknown = Unknown()


class AT01_Test_Browse_The_Api(TestCase):
    '''
    Acceptance test 01
    Test we can browse the API by hopping from one URI to another to
    exercise all the functions defined by the spec, starting from /
    and only using URI's that are returned in responses to us.
    '''
    def setUp(self):
        self.server = Popen(
            'python run_server.py'.split(),
        )


    def tearDown(self):
        self.server.kill()


    def make_request(self, action, url, params=''):
        if not url.startswith(BASE_URI):
            url = BASE_URI + url

        options = '-v -#'
        if params:
            options += ' -d ' + params
        options += ' -X ' + action
        command = 'curl %s %s' % (options, url)
        return check_output(command.split(), stderr=PIPE)


    def post_new_category(self, uri, name):
        response = self.make_request('POST', uri, params='name=%s' % (name,))
        loaded_response = json.loads(response)
        self.assertEqual(
            loaded_response,
            {'name':name, 'uri':unknown}
        )
        uri = loaded_response['uri']
        self.assertTrue(uri.startswith(CATEGORY_URI))
        return uri


    def test_browse_the_api(self):

        # test assumes we start with an empty database
        # setUp should create a test database to ensure this is so

        # Start by requesting the root URI, /
        response = self.make_request('GET', '/')

        # It returns a response containing a list of all top level categories
        # which is empty
        self.assertEquals( json.loads(response), [] )

        # make a post request to the root URL
        # This creates a new top-level category
        response = self.make_request('POST', '/', params='name=Books')

        # The response describes the new category
        loaded_response = json.loads(response)
        self.assertEqual(
            loaded_response,
            {'name':'Books', 'uri':unknown}
        )
        books_uri = loaded_response['uri']
        books_uid = books_uri.split('/')[-1]

        # the new Books category is visible in the list of top level categories
        response = self.make_request('GET', '/')
        loaded_response = json.loads( response )
        self.assertEquals(
            loaded_response,
            [{'name':'Books', 'uri':unknown}]
        )
        self.assertEquals(loaded_response[0]['uri'], books_uri)

        # follow the Books uri to get details information about that category
        response = self.make_request('GET', books_uri)
        loaded = json.loads( response )
        expected = dict(
            name=loaded['name'],
            parent=CATEGORY_URI,
            children=CHILDREN_URI + books_uid,
            lineage=LINEAGE_URI + books_uid,
        )
        self.assertEqual(loaded, expected)
        books_children_uri = loaded['children']

        # post a new Fiction subcategory under Books
        fiction_uri = self.post_new_category(books_children_uri, 'Fiction')

        # post a new Non-Fiction subcategory under Books
        nonfic_uri = self.post_new_category(books_children_uri, 'Non-Fiction')

        # get the Books children uri to check the two new subcategories
        response = self.make_request('GET', books_children_uri)
        loaded = json.loads( response )
        expected = [
            {'name':'Fiction', 'uri':unknown},
            {'name':'Non-Fiction', 'uri':unknown},
        ]
        self.assertEqual(loaded, expected)
        self.assertTrue(loaded[0]['uri'].startswith(CATEGORY_URI))
        self.assertTrue(loaded[1]['uri'].startswith(CATEGORY_URI))

        # post new category 'Geography' under 'Non-Fiction'
        geog_uri = self.post_new_category(nonfic_uri, 'Geography')

        # post new category 'Maps' under 'Geography'
        geog_uri = self.post_new_category(geog_uri, 'Geography')



if __name__ == '__main__':
    main()


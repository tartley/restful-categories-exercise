
import json
from subprocess import check_output, Popen, PIPE, STDOUT
from unittest import TestCase, main

from restful.representation import category_to_json


class Null(object):
    '''
    A file-like object that will silently eat all input, to absorb all
    the stdout produced by web.py while the test runs
    '''
    fileno = lambda _: 0
    def write(*_):
        pass



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
            stdout=Null(),
            stderr=Null(),
        )


    def tearDown(self):
        self.server.kill()


    def make_request(self, url, params=''):
        if params:
            params = ' -d ' + params
        command = 'curl -v -#%s -X %s' % (params, url)
        return check_output(command.split(), stderr=PIPE)


    def test_browse_the_api(self):

        # Start by requesting the root URI, /
        response = self.make_request('GET http://localhost:8080/')

        # It returns a response containing a list of all top level categories
        # which is empty
        self.assertEquals( json.loads(response), [] )

        # make a post request to the root URL
        # This creates a new top-level category
        response = self.make_request(
            'POST http://localhost:8080/', params='name=Books',
        )

        # The response describes the new category
        loaded_response = json.loads(response)
        self.assertTrue( isinstance(loaded_response, dict) )
        self.assertEquals( loaded_response['name'], 'Books')
        books_uri = loaded_response['uri']

        # the new category is visible in list of top level categories
        response = self.make_request('GET http://localhost:8080/')
        #expected = [
        #        {
        #            'uri': 'http://localhost:8080/category/%d' % (electronics.uid,),
        #            'name': 'Electronics',
        #        },
        #        {
        #            'uri': 'http://localhost:8080/category/%d' % (books.uid,),
        #            'name': 'Books',
        #        },
        #    ]
        #self.assertEquals( json.loads(response), expected )






if __name__ == '__main__':
    main()


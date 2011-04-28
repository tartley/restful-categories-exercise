
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


class Unknown(object):
    '''
    Equal to everything. Used as a placeholder for values we don't know
    when comparing collections full of values.
    '''
    def __eq__(*_):
        return True
    def __neq__(*_):
        return False

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
            stdout=Null(),
            stderr=Null(),
        )


    def tearDown(self):
        self.server.kill()


    def make_GET_request(self, url):
        url = 'http://localhost:8080' + url
        command = 'curl -v -# s -X GET %s' % (url,)
        return check_output(command.split(), stderr=PIPE)


    def make_POST_request2(self, url, params=''):
        url = 'http://localhost:8080' + url
        command = 'curl -v -# -d "%s" -X POSTg %s' % (params, url)
        return check_output(command.split(), stderr=PIPE)


    def make_POST_request(self, url, params=''):
        url = 'http://localhost:8080' + url
        if params:
            params = '-d ' + params
        command = 'curl -v -# %s -X POST %s' % (params, url)
        return check_output(command.split(), stderr=PIPE)


    def test_browse_the_api(self):

        # Start by requesting the root URI, /
        response = self.make_GET_request('/')

        # It returns a response containing a list of all top level categories
        # which is empty
        self.assertEquals( json.loads(response), [] )

        # make a post request to the root URL
        # This creates a new top-level category
        response = self.make_POST_request('/', params='name=Books')

        # The response describes the new category
        loaded_response = json.loads(response)
        self.assertTrue( isinstance(loaded_response, dict) )
        self.assertEquals( loaded_response['name'], 'Books')
        books_uri = loaded_response['uri']

        # the new category is visible in list of top level categories
        response = self.make_GET_request('/')
        self.assertEquals(
            json.loads(response),
            [{'name':'Books', 'uri':unknown}]
        )



if __name__ == '__main__':
    main()


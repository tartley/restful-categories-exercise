
import json
from subprocess import check_output, Popen, PIPE, STDOUT
from unittest import TestCase, main

from restful.storage import add, ModelCategory
from restful.storage import books, electronics


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

    def assert_response(self, query, expected_content):
        output = check_output(
            ('curl -v -# -X %s' % (query,)).split(),
            stderr=PIPE,
        )
        self.assertEquals(
            json.loads(output),
            expected_content
        )

    def test_browse_the_api(self):

        # Start by requesting the root URI, /
        # It returns a response containing all top level categories
        self.assert_response(
            'GET http://localhost:8080/',
            [
                {
                    'uri': 'http://localhost:8080/category/%d' % (electronics.uid,),
                    'name': 'Electronics',
                },
                {
                    'uri': 'http://localhost:8080/category/%d' % (books.uid,),
                    'name': 'Books',
                },
            ]
        )


if __name__ == '__main__':
    main()



import json
from subprocess import check_output, Popen, STDOUT
from unittest import TestCase, main

from restful.storage import add, ModelCategory


class Null(object):
    '''
    A file-like object that will silently eat all input, to absorb all
    the stdout produced by web.py while the test runs
    '''
    fileno = lambda _: 0
    def write(*_):
        pass


electronics = ModelCategory('Electronics')
books = ModelCategory('Books')
fiction = ModelCategory('Fiction', books)
nonfiction = ModelCategory('Non-Fiction', books)


def use_test_database():
    # When storage layer is replaced with a DB,
    # this function will just connect to a test DB instead of the live one
    # For now it just populates the DB with some test data
    add(electronics)
    add(books)
    add(fiction)
    add(nonfiction)



class AT01_Test_Browse_The_Api(TestCase):
    '''
    Acceptance test 01
    Test we can browse the API by hopping from one URI to another to
    exercise all the functions defined by the spec, starting from /
    and only using URI's that are returned in responses to us.
    '''
    def setUp(self):
        use_test_database()
        self.server = Popen(
            'python run_server.py'.split(),
            stdout=Null(),
            stderr=Null(),
        )

    def tearDown(self):
        self.server.kill()

    def assert_response(self, query, response_content, status='200 OK'):
        output = check_output(
            ('curl -v -X %s' % (query,)).split(),
            stderr=STDOUT
        )
        self.assertIn('HTTP/1.1 %s' % (status,), output)
        self.assertTrue(
            output.endswith(response_content),
            '"%s" should end with "%s"' % (output, response_content)
        )

    def test_browse_the_api(self):

        # Start by requesting the root URI, /
        # It returns a response containing all top level categories
        self.assert_response(
            'GET http://localhost:8080/',
            json.dumps( [
                {
                    'name': 'Books',
                    'uri': 'http://localhost:8080/category/%d' % (books.uid,)
                },
                {
                    'name': 'Electronics',
                    'uri': 'http://localhost:8080/category/%d' % (electronics.uid,)
                }
            ] )
        )


if __name__ == '__main__':
    main()


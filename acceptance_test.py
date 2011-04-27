
from subprocess import check_output, Popen, STDOUT
from unittest import TestCase, main


class Null(object):
    fileno = lambda _: 0
    def write(*_):
        pass


class AT01_Test_Browse_The_Api(TestCase):

    def setUp(self):
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
        self.assert_response(
            'GET http://localhost:8080/children/2',
            '["Fiction", "Non-Fiction"]'
        )

if __name__ == '__main__':
    main()


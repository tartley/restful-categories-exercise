
from unittest import TestCase

import web
from mock import patch

from server import Children


class TestChildren(TestCase):

    @patch('server.get_subcategories')
    def test_GET_ok(self, mock_get_subcategories):
        Children().GET('123')
        self.assertEqual(mock_get_subcategories.call_args, ((123,), {}))


from __future__ import unicode_literals

import unittest


from click import get_current_context
from erpnext_autoinstall.commands import connect_to_db_wrapper, list_users


class TestBench(unittest.TestCase):
    def setUp(self):
        self.context = get_current_context()

    def test_is_username_exists_wrapper(self):
        list_users()
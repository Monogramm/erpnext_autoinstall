from __future__ import unicode_literals

import unittest

from erpnext_autoinstall.commands.wrappers import connect_to_db_wrapper, is_email_exists_wrapper, _checker


class TestWrappers(unittest.TestCase):
    def test_is_email_exists_wrapper(self):
        f = is_email_exists_wrapper(_checker)
        f({'username': "Administrator", 'email': "guest@example.com", 'roles': ("Auditor",)})
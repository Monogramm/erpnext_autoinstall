from __future__ import unicode_literals

import unittest

from erpnext_autoinstall.commands.wrappers import email_exists, _checker


class TestWrappers(unittest.TestCase):
    def test_all_wrappers(self):
        f = email_exists(_checker)
        f(username="Administrator", email="guest@example.com", roles= ("Auditor", ))
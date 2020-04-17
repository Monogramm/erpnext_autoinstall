from __future__ import unicode_literals

import unittest

import frappe
from erpnext_autoinstall.commands.wrappers import email_exists, _checker


class TestWrappers(unittest.TestCase):
    def test_all_wrappers(self):
        f = email_exists(_checker)
        if frappe.__version__[:2] == "10":
            self.assertIsNone(f(username="Administrator", email="guest@example.com", roles=("System Manager", )))
        else:
            self.assertIsNone(f(username="Administrator", email="guest@example.com", roles=("Translator",)))
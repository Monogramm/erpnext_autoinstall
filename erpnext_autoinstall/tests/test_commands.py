from __future__ import unicode_literals

import sys
import unittest

import os

from click import get_current_context


class TestBench(unittest.TestCase):
    def setUp(self):
        self.context = get_current_context()

    def test_set_user_permissions_validation_of_user(self):
        code = os.system("cd ..; bench set-user-permissions Administrator System Manager")
        self.assertEqual(code, 0)

    def test_list_users(self):
        code = os.system("cd ..; bench list-users")
        self.assertEqual(code, 0)
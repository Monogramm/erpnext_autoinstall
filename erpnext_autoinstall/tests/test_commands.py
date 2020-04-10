from __future__ import unicode_literals

import sys
import unittest

from click import get_current_context
from erpnext_autoinstall.commands import set_user_permissions


class TestBench(unittest.TestCase):
    def setUp(self):
        self.context = get_current_context()

    def set_user_permissions_validation_of_user(self):
        set_user_permissions(self.context, "fdsaa", "Auditor")
        output = sys.stdout.getline().strip()
        self.assertEqual(output, "Error: Username fdsaa does not exist")

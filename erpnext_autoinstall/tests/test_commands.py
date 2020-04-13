from __future__ import unicode_literals

import unittest


from erpnext_autoinstall.commands import _set_user_permissions


class TestCommands(unittest.TestCase):
    def test_set_user_permissions_admin(self):
        _set_user_permissions('Administrator', 'System Manager')

    def test_set_user_permissions_none(self):
        _set_user_permissions(None, 'System Manager')

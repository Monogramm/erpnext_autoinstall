from __future__ import unicode_literals

import sys
import unittest

import frappe
from erpnext_autoinstall.commands import _set_user_permissions, _create_user, _list_users, _delete_user, \
    _set_user_password


def get_hash_password_from_user(usr, data):
    for d in data:
        if d[0] == usr:
            old_key = d[1]
    return old_key


class TestCommands(unittest.TestCase):
    def setUp(self):
        self.user_email = 'test@mail.ru'

    def test_set_user_permissions_admin(self):
        _set_user_permissions('Administrator', ('System Manager',))

    def test_set_user_permissions_none(self):
        self.assertRaises(frappe.ValidationError, _set_user_permissions, None, 'System Manager')

    def test_create_delete_user_is_exists(self):
        if frappe.db.exists("User", self.user_email):
            frappe.get_doc("User", self.user_email).delete()
        _create_user('test', self.user_email, 'Test', 'User')
        self.assertIsNotNone(frappe.get_doc("User", self.user_email))
        _delete_user('test', True)
        self.assertIsNone(frappe.db.exists("User", self.user_email))

    def test_list_users(self):
        _list_users('Administrator')

    def test_set_user_password(self):
        if not frappe.db.exists("User", self.user_email):
            _create_user('test', self.user_email, 'Test', 'User')
        data = frappe.db.sql("""SELECT name, password FROM `__Auth`""")
        old_hash_password = get_hash_password_from_user('test', data)
        _set_user_password("test", 'password')
        new_hash_password = get_hash_password_from_user('test',
                                                        frappe.db.sql("""SELECT name, password FROM `__Auth`"""))
        self.assertNotEqual(old_hash_password, new_hash_password)
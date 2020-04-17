from __future__ import unicode_literals

import unittest
import frappe

from erpnext_autoinstall.commands import _set_user_permissions, _add_user, \
    _set_user_password, _set_user_role, _delete_user


def get_hash_password_from_user(usr, data):
    old_key = None
    for d in data:
        if d[0] == usr:
            old_key = d[1]
    if old_key is None:
        frappe.throw("old key is None")
    return old_key


class TestCommands(unittest.TestCase):
    def setUp(self):
        self.test_user_email = 'test@mail.ru'
        self.test_user_name = 'test'
        if not frappe.db.exists("User", self.test_user_email):
            _add_user("test", self.test_user_email, "Test", "User")

    def test_set_user_permissions_admin(self):
        _set_user_permissions('Administrator', ('System Manager',))
        self.assertIn("System Manager", frappe.get_roles("Administrator"))

    def test_set_user_permissions_none(self):
        self.assertRaises(frappe.ValidationError, _set_user_permissions, None, 'System Manager')

    def test_create_delete_user_is_exists(self):
        if not frappe.db.exists("User", "test_creation@mail.ru"):
            _add_user('test_creation', "test_creation@mail.ru", 'Test', 'User')
        self.assertIsNotNone(frappe.get_doc("User", "test_creation@mail.ru"))
        _delete_user('test_creation', True)
        self.assertIsNone(frappe.db.exists("User", "test_creation@mail.ru"))

    def test_set_user_password(self):
        _set_user_password("test", "raw_password")
        data = frappe.db.sql("""SELECT name, password FROM `__Auth`""")
        old_hash_password = get_hash_password_from_user('test', data)
        _set_user_password("test", 'password')
        new_hash_password = get_hash_password_from_user('test',
                                                        frappe.db.sql("""SELECT name, password FROM `__Auth`"""))
        self.assertNotEqual(old_hash_password, new_hash_password)

    def test_user_role(self):
        if not frappe.db.exists("Role Profile", "Test 1"):
            new_role_profile = frappe.get_doc(dict(doctype='Role Profile', role_profile='Test 1')).insert()
        else:
            new_role_profile = frappe.get_doc("Role Profile", "Test 1")

        self.assertEqual(new_role_profile.role_profile, 'Test 1')

        # add role
        new_role_profile.append("roles", {
            "role": 'System Manager'
        })
        new_role_profile.save()
        _set_user_role("test", "Test 1")
        #if frappe.db.exists("Role Profile", "Test 1"):
        #    frappe.get_doc("Role Profile", 'Test 1').delete()

from __future__ import unicode_literals

import unittest

import frappe
from erpnext_autoinstall.commands import _set_user_permissions, _create_user, _list_users, _delete_user, \
    _set_user_password, _set_user_role


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
        self.user_email_2 = "test2@mail.ru"

        self.user_email = 'test@mail.ru'
        self.test_user = frappe.get_doc(
            {"doctype": "User", 'name': "test", "email": self.user_email, "first_name": "Test", "last_name": "User",
             "enabled": 1, "send_welcome_email": 0, })
        self.test_user.flags.ignore_validate = True
        if not frappe.db.exists("User", self.user_email):
            self.test_user.insert()
            self.test_user.add_roles("System Manager")

    def test_set_user_permissions_admin(self):
        _set_user_permissions('Administrator', ('System Manager',))

    def test_set_user_permissions_none(self):
        self.assertRaises(frappe.ValidationError, _set_user_permissions, None, 'System Manager')

    def test_create_delete_user_is_exists(self):
        #_create_user('test2', "test2@mail.ru", 'Test2', 'User')
        #self.assertIsNotNone(frappe.get_doc("User", "test2@mail.ru"))
        #_delete_user('test2', True)
        #self.assertIsNone(frappe.db.exists("User", "test2@mail.ru"))
        print('fdsa')

    def test_list_users(self):
        _list_users('Administrator')

    def test_set_user_password(self):
        if not frappe.db.exists("User", self.user_email_2):
            _create_user('test2', self.user_email_2, 'Test', 'User')
        _set_user_password("test2", "raw_password")
        data = frappe.db.sql("""SELECT name, password FROM `__Auth`""")
        old_hash_password = get_hash_password_from_user('test2', data)
        _set_user_password("test2", 'password')
        new_hash_password = get_hash_password_from_user('test2',
                                                        frappe.db.sql("""SELECT name, password FROM `__Auth`"""))
        self.assertNotEqual(old_hash_password, new_hash_password)

    def test_user_role(self):
        if not frappe.db.exists("User", self.user_email_2):
            _create_user('test2', self.user_email_2, 'Test', 'User')

        new_role_profile = frappe.get_doc(dict(doctype='Role Profile', role_profile='Test 5')).insert()

        self.assertEqual(new_role_profile.role_profile, 'Test 5')

        # add role
        new_role_profile.append("roles", {
            "role": 'Auditor'
        })
        new_role_profile.save()
        _set_user_role("test2", "Test 5")
        if frappe.db.exists("Role Profile", "Test 5"):
            frappe.get_doc("Role Profile", 'Test 5').delete()

    def tearDown(self):
        self.test_user.delete()
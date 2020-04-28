# -*- coding: utf-8 -*-
# Copyright (c) 2020, Monogramm and Contributors
# See license.txt

from __future__ import unicode_literals

import unittest
import frappe

from erpnext_autoinstall.commands import commands, _list_users, _delete_user, \
    _add_user, _set_user_password, _set_user_roles, _set_user_role_profile, _get_user_api_secret


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
        self.test_user_name = 'test'
        self.test_user_email = 'test@mail.ru'

        if not frappe.db.exists('User', self.test_user_email):
            user_doc = frappe.get_doc(
                {"doctype": 'User', 'username': self.test_user_name,
                 "email": self.test_user_email,
                 "first_name": self.test_user_name,
                 "enabled": 1, "send_welcome_email": 0})
            user_doc.insert()
            frappe.db.commit()

        self.test_delete_user_name = 'test_delete'
        self.test_delete_user_email = 'test_delete@mail.ru'

        if not frappe.db.exists('User', self.test_delete_user_email):
            user_doc = frappe.get_doc(
                {"doctype": 'User', 'username': self.test_delete_user_name,
                 "email": self.test_delete_user_email,
                 "first_name": self.test_delete_user_name,
                 "enabled": 1, "send_welcome_email": 0})
            user_doc.insert()
            frappe.db.commit()

        self.test_add_user_name = 'test_add'
        self.test_add_user_email = 'test_add@mail.ru'

        self.test_role_profile = 'Test Commands'
        if not frappe.db.exists('Role Profile', self.test_role_profile):
            self.new_role_profile = frappe.get_doc(
                dict(doctype='Role Profile', role_profile=self.test_role_profile)).insert()
        else:
            self.new_role_profile = frappe.get_doc(
                'Role Profile', self.test_role_profile)

        self.assertEqual(self.new_role_profile.role_profile,
                         self.test_role_profile)

        self.new_role_profile.append("roles", {
            "role": 'System Manager'
        })
        self.new_role_profile.save()

    def tearDown(self):
        if frappe.db.exists('User', self.test_user_email):
            user = frappe.get_doc('User', {'username': self.test_user_name})
            user.delete()
            frappe.db.commit()

        if frappe.db.exists('User', self.test_delete_user_email):
            user = frappe.get_doc(
                'User', {'username': self.test_delete_user_name})
            user.delete()
            frappe.db.commit()

        if frappe.db.exists('User', self.test_add_user_email):
            user = frappe.get_doc(
                'User', {'username': self.test_add_user_name})
            user.delete()
            frappe.db.commit()

        if frappe.db.exists('Role Profile', self.test_role_profile):
            frappe.get_doc('Role Profile', self.test_role_profile).delete()

    def test_commands(self):
        self.assertNotEqual(len(commands), 0)

    def test_list_users(self):
        users = _list_users(None, None)
        self.assertIn({'name': self.test_user_email}, users)

    def test_list_users_with_username(self):
        users = _list_users(self.test_user_name, None)
        self.assertIn({'name': self.test_user_email}, users)

    def test_list_users_with_email(self):
        users = _list_users(None, self.test_user_email)
        self.assertIn({'name': self.test_user_email}, users)

    def test_list_users_with_username_and_email(self):
        users = _list_users(self.test_user_name, self.test_user_email)
        self.assertIn({'name': self.test_user_email}, users)

    def test_list_users_not_found(self):
        users = _list_users(self.test_user_name + '42', None)
        self.assertEqual(len(users), 0)

    def test_delete_user(self):
        _delete_user(self.test_delete_user_name, True)
        self.assertIsNone(frappe.db.exists(
            'User', self.test_delete_user_email))

    def test_delete_user_not_exist(self):
        self.assertRaises(frappe.DoesNotExistError, _delete_user,
                          self.test_delete_user_name + '42', True)

    def test_add_user(self):
        _add_user(self.test_add_user_name, self.test_add_user_email,
                  self.test_add_user_name, self.test_add_user_name)
        self.assertTrue(frappe.db.exists('User', self.test_add_user_email))

    def test_add_user_already_exist(self):
        self.assertRaises(frappe.DuplicateEntryError, _add_user, self.test_user_name,
                          self.test_user_email, self.test_user_name, self.test_user_name)

    def test_set_user_password(self):
        _set_user_password(self.test_user_name, 'raw_password')
        data = frappe.db.sql("""SELECT name, password FROM `__Auth`""")
        old_hash_password = get_hash_password_from_user(
            self.test_user_name, data)

        _set_user_password(self.test_user_name, 'password')
        data = frappe.db.sql("""SELECT name, password FROM `__Auth`""")
        new_hash_password = get_hash_password_from_user(
            self.test_user_name, data)

        self.assertNotEqual(old_hash_password, new_hash_password)

    def test_set_user_roles(self):
        _set_user_roles(self.test_user_name, ('System Manager',))
        self.assertIn('System Manager', frappe.get_roles(self.test_user_email))

    def test_set_user_roles_none(self):
        self.assertRaises(frappe.ValidationError,
                          _set_user_roles, None, 'System Manager')

    def test_set_user_role_profile(self):
        _set_user_role_profile(self.test_user_name, self.test_role_profile)
        self.assertEqual(frappe.get_doc(
            'User', self.test_user_email).role_profile_name, self.test_role_profile)

    def test_get_user_api_secret_not_none(self):
        secret_key = _get_user_api_secret("Administrator")
        self.assertIsNotNone(secret_key)

    def test_get_user_api_secret_does_not_exists(self):
        self.assertRaises(frappe.DoesNotExistError, _get_user_api_secret,
                          "Alien42")

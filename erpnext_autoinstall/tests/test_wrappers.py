# -*- coding: utf-8 -*-
# Copyright (c) 2020, Monogramm and Contributors
# See license.txt

from __future__ import unicode_literals

import unittest
import frappe

from erpnext_autoinstall.commands.wrappers import email_exists, username_exists, roles_exist, role_profile_exists


@email_exists
def _checker_email_exists(email):
    #print("Email {}".format(email))
    return email


@username_exists
def _checker_username_exists(username):
    #print("Username {} ".format(username))
    return username


@roles_exist
def _checker_roles_exist(roles):
    #print("Roles {}".format(roles))
    return roles


@role_profile_exists
def _checker_role_profile(role_profile):
    #print("Role profile {}".format(roles))
    return role_profile


class TestWrappers(unittest.TestCase):
    def setUp(self):
        self.test_role_profile = 'Test Wrappers'
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
        if frappe.db.exists('Role Profile', self.test_role_profile):
            frappe.get_doc('Role Profile', self.test_role_profile).delete()

    def test_email_exists(self):
        f = email_exists(_checker_email_exists)
        self.assertIsNone(f(email="guest@example.com"))

    def test_email_not_exists(self):
        f = email_exists(_checker_email_exists)
        self.assertRaises(SystemExit, f, email="guest42@example.com")

    def test_username_exists(self):
        f = username_exists(_checker_username_exists)
        self.assertIsNone(f(username="Administrator"))

    def test_username_not_exists(self):
        f = username_exists(_checker_username_exists)
        self.assertRaises(SystemExit, f, username="Administrator42")

    def test_roles_exist(self):
        f = roles_exist(_checker_roles_exist)
        if frappe.__version__[:2] == "10":
            self.assertIsNone(f(roles=("System Manager", )))
        else:
            self.assertIsNone(f(roles=("Translator", )))

    def test_roles_not_exist(self):
        f = roles_exist(_checker_roles_exist)
        self.assertRaises(SystemExit, f, roles=("Alien42", ) )

    def test_role_profile_exists(self):
        f = role_profile_exists(_checker_role_profile)
        self.assertIsNone(f(role_profile=self.test_role_profile))

    def test_role_profile_not_exists(self):
        f = role_profile_exists(_checker_role_profile)
        self.assertRaises(SystemExit, f, role_profile=self.test_role_profile + '42')

# -*- coding: utf-8 -*-
# Copyright (c) 2020, Monogramm and Contributors
# See license.txt

"""Custom bench commands."""

from __future__ import unicode_literals, absolute_import

import click
import frappe
from click import pass_context
import getpass

from frappe.utils.password import update_password

from erpnext_autoinstall.commands.wrappers import connect_to_db, \
    username_exists, roles_exist, role_profile_exists


def _add_user_api_key(username):
    from frappe.core.doctype.user.user import generate_keys
    if frappe.db.exists("User", {"username": username}):
        generate_keys(frappe.get_value('User', {'username': username}, 'name'))
        frappe.db.commit()
        print("API key generated for user {}".format(username))
        return 0


def _get_user_api_key(username):
    if frappe.db.exists("User", {"username": username}):
        user_details = frappe.get_doc("User", {'username': username})
        if user_details.api_key:
            print(user_details.api_key)
            return user_details.api_key


def _get_user_api_secret(username):
    if frappe.db.exists('User', {'username': username}):
        user_details = frappe.get_doc("User", {'username': username})
        if user_details.api_secret:
            generated_secret = frappe.utils.password.get_decrypted_password(
                "User", username, fieldname='api_secret'
            )
            print(generated_secret)
            return generated_secret


def _list_users(username=None, email=None):
    filters = []

    if username is not None:
        filters.append({'username': username})

    if email is not None:
        filters.append({'email': email})

    users = frappe.get_all("User", filters=filters)
    for user in users:
        print(user.name)

    return users


@click.command('list-users', help="List users in site")
@click.option('--username', help='name of user')
@click.option('--email', help='email of user')
@pass_context
@connect_to_db
def list_users(username=None, email=None):
    """Display list of users."""
    _list_users(username, email)


def _delete_user(username, force):
    if not force:
        answer = input(
            'Are you sure you want to delete user {} (y/N): '.format(username))
        if answer in ('N', 'n'):
            return
        if answer in ('y', 'Y'):
            user = frappe.get_doc("User", {'username': username})
    else:
        user = frappe.get_doc("User", {'username': username})
    user.delete()
    frappe.db.commit()


@click.command('delete-user', help="Delete a user from a site")
@click.argument('username')
@click.option('--force', is_flag=True, help='Pass confirmation')
@pass_context
@connect_to_db
@username_exists
def delete_user(username, force=False):
    """Delete user from database."""
    _delete_user(username, force)


def _add_user(username, email, firstname, lastname):
    if not firstname:
        firstname = input("First name: ")
    if not lastname:
        lastname = input("Last name: ")

    user_doc = frappe.get_doc(
        {"doctype": "User", 'username': username, "email": email,
         "first_name": firstname, "last_name": lastname,
         "enabled": 1, "send_welcome_email": 0})
    user_doc.insert()
    frappe.db.commit()


@click.command('add-user', help="Add a new user to a site")
@click.argument('username')
@click.argument('email')
@click.option('--firstname', help="First name")
@click.option('--lastname', help="Last name")
@pass_context
@connect_to_db
def add_user(username, email, firstname=None, lastname=None):
    """Create new user in database."""
    _add_user(username, email, firstname, lastname)


def _set_user_password(username, password):
    if password is None:
        password = getpass.getpass('Please, enter new password for username {}: '
                                   .format(username))
        confirmed_password = getpass.getpass('Confirm new password for username {}: '
                                             .format(username))
        if password == confirmed_password:
            update_password(username, password, logout_all_sessions=True)
            frappe.db.commit()
        else:
            print("Confirmed password is not valid")
    else:
        update_password(username, password, logout_all_sessions=True)
        frappe.db.commit()


@click.command('set-user-password', help="Set a user password")
@click.argument('username')
@click.option('--password', help='Set password')
@pass_context
@connect_to_db
@username_exists
def set_user_password(username, password):
    """Update user password."""
    _set_user_password(username, password)


def _set_user_roles(username=None, roles=None):
    if username is not None:
        user = frappe.get_doc("User", {'username': username})
        for role in roles:
            user.add_roles(role)

        frappe.db.commit()
    else:
        frappe.throw("Set the username")


@click.command('set-user-roles', help="Set a user's roles")
@click.argument('username')
@click.argument('roles', nargs=-1)
@pass_context
@connect_to_db
@username_exists
@roles_exist
def set_user_roles(username=None, roles=None):
    """Set roles for user."""
    _set_user_roles(username, roles)


def _set_user_role_profile(username, role):
    if username is not None:
        user = frappe.get_doc("User", {'username': username})
        user.role_profile_name = role
        user.save()
        frappe.db.commit()


@click.command('set-user-role-profile', help="Set a user's role profile")
@click.argument('username')
@click.argument('role')
@pass_context
@connect_to_db
@role_profile_exists
@username_exists
def set_user_role_profile(username, role_profile):
    """Set role profile for user."""
    _set_user_role_profile(username, role_profile)



@click.command('add-user-api-key', help="Add a new API key to a user")
@click.argument("username")
@pass_context
@connect_to_db
def add_user_api_key(username):
    """Generate a user's API key."""
    _add_user_api_key(username)


@click.command('get-user-api-key', help="Get API key")
@click.argument("username")
@pass_context
@connect_to_db
def get_user_api_key(username):
    """Get a user's API key."""
    _get_user_api_key(username)


@click.command('get-user-api-secret', help="Generate API secret")
@click.argument("username")
@pass_context
@connect_to_db
def get_user_api_secret(username):
    """Get a user's API secret."""
    _get_user_api_secret(username)


commands = [list_users, delete_user, add_user, set_user_password, set_user_roles, set_user_role_profile,
            add_user_api_key, get_user_api_key, get_user_api_secret]

"""Custom bench commands."""

from __future__ import unicode_literals, absolute_import

import click
import frappe
from click import pass_context
import getpass

from erpnext_autoinstall.commands.wrappers import connect_to_db, \
    username_exists, roles_exist, role_profile_exists
from frappe.utils.password import update_password


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


@click.command('list-users', help="Show list of users")
@click.option('--username', help='name of user')
@click.option('--email', help='email of user')
@pass_context
@connect_to_db
def list_users(username=None, email=None):
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


@click.command('delete-user', help='Delete user from database')
@click.argument('username')
@click.option('--force', is_flag=True, help='Pass confirmation')
@pass_context
@connect_to_db
@username_exists
def delete_user(username, force=False):
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


@click.command('add-user', help='Create new user')
@click.argument('username')
@click.argument('email')
@click.option('--firstname', help="First name")
@click.option('--lastname', help="Last name")
@pass_context
@connect_to_db
def add_user(username, email, firstname=None, lastname=None):
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


@click.command('set-user-password', help='Update user password')
@click.argument('username')
@click.option('--password', help='Set password')
@pass_context
@connect_to_db
@username_exists
def set_user_password(username, password):
    _set_user_password(username, password)


def _set_user_roles(username=None, roles=None):
    if username is not None:
        user = frappe.get_doc("User", {'username': username})
        for role in roles:
            user.add_roles(role)

        frappe.db.commit()
    else:
        frappe.throw("Set the username")


@click.command('set-user-roles', help="Set roles for user")
@click.argument('username')
@click.argument('roles', nargs=-1)
@pass_context
@connect_to_db
@username_exists
@roles_exist
def set_user_roles(username=None, roles=None):
    _set_user_roles(username, roles)


def _set_user_role_profile(username, role):
    if username is not None:
        user = frappe.get_doc("User", {'username': username})
        user.role_profile_name = role
        user.save()
        frappe.db.commit()


@click.command('set-user-role-profile', help="Set user role profile")
@click.argument('username')
@click.argument('role')
@pass_context
@connect_to_db
@role_profile_exists
@username_exists
def set_user_role_profile(username, role_profile):
    _set_user_role_profile(username, role_profile)


commands = [list_users,
            delete_user, add_user, set_user_password, set_user_roles, set_user_role_profile]

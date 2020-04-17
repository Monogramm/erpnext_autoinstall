from __future__ import unicode_literals, absolute_import

import click
import frappe
from click import pass_context
import getpass

from erpnext_autoinstall.commands.wrappers import connect_to_db, \
    username_exists, roles_exist, role_profile_exists
from frappe.utils.password import update_password


def _set_user_permissions(username=None, permissions=None):
    if username is not None:
        user = frappe.get_doc("User", {'username': username})
        try:
            for role in permissions:
                user.add_roles(role)
            frappe.db.commit()
        finally:
            frappe.destroy()
    else:
        frappe.throw("Set the user name")


def _set_user_role(username, role):
    if username is not None:
        user = frappe.get_doc("User", {'username': username})
        user.role_profile_name = role
        try:
            user.save()
            frappe.db.commit()
        finally:
            frappe.destroy()


def _create_user(username, email, firstname, lastname):
    if not firstname:
        firstname = input("First name: ")
    if not lastname:
        lastname = input("Last name: ")

    user_doc = frappe.get_doc(
        {"doctype": "User", 'username': username, "email": email,
         "first_name": firstname, "last_name": lastname,
         "enabled": 1, "send_welcome_email": 0})
    try:
        user_doc.insert()
        frappe.db.commit()
    finally:
        frappe.destroy()


def _list_users(username=None, email=None):
    users = frappe.get_all("User", filters=[{'username': username}, {'email': email}])
    for user in users:
        print(user.name)
    return users


@click.command('set-user-permissions', help="Set permissions for user")
@click.argument('username')
@click.argument('roles', nargs=-1)
@pass_context
@connect_to_db
@username_exists
@roles_exist
def set_user_permissions(username=None, roles=None):
    _set_user_permissions(username, roles)


@click.command('set-user-role', help="Set user role")
@click.argument("username")
@click.argument('role')
@pass_context
@connect_to_db
@role_profile_exists
@username_exists
def set_user_role(username, role):
    _set_user_role(username, role)


@click.command('list-users', help="Show list of users")
@click.option('--username', help='name of user')
@click.option('--email', help='email of user')
@pass_context
@connect_to_db
def list_users(username=None, email=None):
    """Show list of users."""
    _list_users(username, email)


def _set_user_password(username, password):
    if password is None:
        password = getpass.getpass('Please, enter new password for username {}: '
                                   .format(username))
        confirmed_password = getpass.getpass('Confirm new password for username {}: '
                                             .format(username))
        if password == confirmed_password:
            try:
                update_password(username, password, logout_all_sessions=True)
                frappe.db.commit()
            finally:
                frappe.destroy()
        else:
            print("Confirmed password is not valid")
    else:
        try:
            update_password(username, password, logout_all_sessions=True)
            frappe.db.commit()
        finally:
            frappe.destroy()


def _delete_user(username, force):
    if not force:
        ans = input('Are you sure you want to delete user {} (y/N): '.format(username))
        if ans in ('N', 'n'):
            return
        if ans in ('y', 'Y'):
            user = frappe.get_doc("User", {'username': username})
    else:
        user = frappe.get_doc("User", {'username': username})
    try:
        user.delete()
        frappe.db.commit()
    finally:
        frappe.destroy()


@click.command('set-user-password', help='Update user password')
@click.argument('username')
@click.option('--password', help='Set password')
@pass_context
@connect_to_db
@username_exists
def set_user_password(username, password):
    _set_user_password(username, password)


@click.command('delete-user', help='Delete user from database')
@click.argument('username')
@click.option('--force', is_flag=True, help='Pass confirmation')
@pass_context
@connect_to_db
@username_exists
def delete_user(username, force=False):
    _delete_user(username, force)


@click.command('add-user', help='Create new user')
@click.argument('username')
@click.argument('email')
@click.option('--firstname', help="First name")
@click.option('--lastname', help="Last name")
@pass_context
@connect_to_db
def create_user(username, email, firstname=None, lastname=None):
    _create_user(username, email, firstname, lastname)


commands = [set_user_permissions,
            list_users, set_user_password, delete_user, create_user, set_user_role]

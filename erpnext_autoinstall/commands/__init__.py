from __future__ import unicode_literals, absolute_import

import sys

import click
import frappe
from click import pass_context
import getpass

from erpnext_autoinstall.commands.wrappers import connect_to_db_wrapper, is_email_exists_wrapper, \
    is_username_exists_wrapper, is_roles_exist_wrapper
from frappe.client import insert
from frappe.model.db_schema import DbManager
from frappe.utils.password import update_password


# @click.command('set-user-role')
# @click.argument('username')
# @click.argument('role')
# @pass_context
# def set_user_role(username=None, roles=None):
#

def _set_user_permissions(username=None, roles=None):
    if username is not None:
        user = frappe.get_doc("User", {'username': username})
        for role in roles:
            user.add_roles(role)

@click.command('set-user-permissions', help="Set permissions for user")
@click.argument('username')
@click.argument('roles', nargs=-1)
@pass_context
@connect_to_db_wrapper
@is_username_exists_wrapper
@is_roles_exist_wrapper
def set_user_permissions(username=None, roles=None):
    _set_user_permissions(username, roles)

@click.command('list-users', help="Show list of users")
@click.option('--username', help='name of user')
@click.option('--email', help='email of user')
@pass_context
@connect_to_db_wrapper
def list_users(username=None, email=None, app=None):
    """
    Show list of users
    """
    users = frappe.get_all("User", filters=[{'username': username}, {'email': email}])
    for user in users:
        print(user.name)


@click.command('set-user-password', help='Update user password')
@click.argument('username')
@click.option('--password', help='Set password')
@pass_context
@connect_to_db_wrapper
@is_username_exists_wrapper
def set_user_password(username, password):
    if password is None:
        password = getpass.getpass('Please, enter new password for username {}: '.format(username))
        confirmed_password = getpass.getpass('Confirm new password for username {}: '.format(username))
        if password == confirmed_password:
            update_password(username, password, logout_all_sessions=True)
        else:
            print("Confirmed password is not valid")
    else:
        update_password(username, password, logout_all_sessions=True)


@click.command('delete-user', help='Delete user from database')
@click.argument('username')
@click.option('--force', is_flag=True, help='Pass confirmation')
@pass_context
@connect_to_db_wrapper
@is_username_exists_wrapper
def delete_user(username, force=False):
    if not force:
        ans = input('Are you sure you want to delete user {} (y/N): '.format(username))
        if ans is None or ans == 'N' or ans == 'n':
            return
        if ans == 'y' or ans == 'Y':
            frappe.get_doc("User", {'username': username}).delete()
    else:
        frappe.get_doc("User", {'username': username}).delete()


@click.command('create-user', help='Create new user')
@click.argument('username')
@click.argument('email')
@click.option('--firstname')
@click.option('--lastname')
@pass_context
@connect_to_db_wrapper
def create_user(username, email, firstname=None, lastname=None):
    if not firstname:
        firstname = input("First name: ")
    if not lastname:
        lastname = input("Last name: ")
    frappe.get_doc(
        {"doctype": "User", 'name': username, "email": email, "first_name": firstname, "last_name": lastname,
         "enabled": 0}).insert()


commands = [set_user_permissions, list_users, set_user_password, delete_user, create_user]

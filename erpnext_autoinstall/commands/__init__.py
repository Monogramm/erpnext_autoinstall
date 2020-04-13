from __future__ import unicode_literals, absolute_import

import sys

import click
import frappe
from click import pass_context
import getpass

from erpnext_autoinstall.commands.wrappers import connect_to_db_wrapper, is_email_exists_wrapper, \
    is_username_exists_wrapper, is_roles_exist_wrapper
from frappe.utils.password import update_password


@click.command('set-user-permissions')
@click.argument('username')
@click.argument('roles', nargs=-1)
@pass_context
@connect_to_db_wrapper
@is_username_exists_wrapper
@is_roles_exist_wrapper
def set_user_permissions(username=None, roles=None):
    if username is not None:
        user = frappe.get_doc("User", {'username': username})
        for role in roles:
            user.add_roles(role)


@click.command('list-users')
@click.option('--username', help='name of user')
@click.option('--email', help='email of user')
@pass_context
@connect_to_db_wrapper
def list_users(username=None, email=None):
    users = frappe.get_all("User", filters=[{'username': username}, {'email': email}])
    for user in users:
        print(user.name)


@click.command('set-user-password')
@click.argument('username')
@click.option('--password', help='set password')
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


@click.command('delete-user')
@click.argument('username')
@click.option('--force', is_flag=True, help='pass confirmation')
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


commands = [set_user_permissions, list_users, set_user_password, delete_user]
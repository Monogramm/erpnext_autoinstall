from __future__ import unicode_literals, absolute_import

import sys

import click
import frappe
from click import pass_context
import getpass

from frappe.utils.password import update_password


def is_username_exists(username):
    if not frappe.db.exists('User', {'username': username}):
        print("Error: Username {} does not exist".format(username))
        return False
    return True


def is_email_exists(email):
    if not frappe.db.exists('User', email):
        print("Error: Email {} does not exist".format(email))
        return False
    return True


def is_role_exists(role):
    if not frappe.db.exists('Role', role):
        print("Error: Role {} does not exist".format(role))
        return False
    return True


def wrapper_set_user_permissions(set_user_permissions):
    def accept_arguments(context, username=None, roles=None):
        connect_to_db(context)
        if not is_username_exists(username):
            sys.exit()

        for role in roles:
            if not is_role_exists(role):
                return
        set_user_permissions(username, roles)

    return accept_arguments


def wrapper_list_users(list_users):
    def accept_arguments(context, username, email):
        connect_to_db(context)
        if username is not None and not is_username_exists(username) or (email is not None and not is_email_exists(
                email)):
            return
        list_users(username, email)

    return accept_arguments


def wrapper_set_user_password(set_user_password):
    def accept_arguments(context, username, password=None):
        connect_to_db(context)
        if not is_username_exists(username):
            return
        if password is None:
            password = getpass.getpass('Please, enter new password for username {}: '.format(username))
            confirmed_password = password = getpass.getpass('Confirm new password for username {}: '.format(username))
            if password == confirmed_password:
                set_user_password(username, password)
            else:
                print("Confirmed password is not valid")
        else:
            set_user_password(username, password)

    return accept_arguments


def connect_to_db(context):
    site = context.obj['sites'][0]
    frappe.init(site=site)
    frappe.connect(site)


@click.command('set-user-permissions')
@click.argument('username')
@click.argument('roles', nargs=-1)
@pass_context
@wrapper_set_user_permissions
def set_user_permissions(username=None, roles=None):
    if username is not None:
        user = frappe.get_doc("User", {'username': username})
        for role in roles:
            user.add_roles(role)


@click.command('list-users')
@click.option('--username', help='name of user')
@click.option('--email', help='email of user')
@pass_context
@wrapper_list_users
def list_users(username=None, email=None):
    users = frappe.get_all("User", filters=[{'username': username}, {'email': email}])
    for user in users:
        print(user.name)


@click.command('set-user-password')
@click.argument('username')
@click.option('--password', help='set password')
@pass_context
@wrapper_set_user_password
def set_user_password(username, password):
    update_password(username, password, logout_all_sessions=True)


def wrapper_delete_user(delete_user):
    def accept_arguments(context, username, force=False):
        connect_to_db(context)
        if not force:
            ans = input('Are you sure you want to delete user {} (y/N): '.format(username))
            if ans is None or ans == 'N' or ans == 'n':
                return
            if ans == 'y' or ans == 'Y':
                delete_user(username)
        else:
            delete_user(username)

    return accept_arguments


@click.command('delete-user')
@click.argument('username')
@click.option('--force', is_flag=True, help='pass confirmation')
@pass_context
@wrapper_delete_user
def delete_user(username):
    frappe.get_doc("User", {'username': username}).delete()


commands = [set_user_permissions, list_users, set_user_password, delete_user]

from __future__ import unicode_literals, absolute_import
import click
import frappe
from click import pass_context


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
    def accept_argument(context, username=None, roles=None):
        connect_to_db(context)
        if not is_username_exists(username):
            return

        for role in roles:
            if not is_role_exists(role):
                return
        set_user_permissions(username, roles)

    return accept_argument


def wrapper_list_users(list_users):
    def accept_argument(context, username, email):
        connect_to_db(context)
        if username is not None and not is_username_exists(username) or (email is not None and not is_email_exists(
                email)):
            return
        list_users(username, email)

    return accept_argument


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
@click.option('--username')
@click.option('--email')
@pass_context
@wrapper_list_users
def list_users(username=None, email=None):
    users = frappe.get_all("User", filters=[{'username': username}, {'email': email}])
    for user in users:
        print(user.name)


commands = [set_user_permissions, list_users]

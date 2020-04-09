from __future__ import unicode_literals, absolute_import
import click
import frappe
from click import pass_context
from frappe.utils.user import add_role


# def wrapper_set_user_permissions(set_user_permissions):
#     def accept_argument(context, username=None, email=None, role=None):
#         if email is not None and frappe.db.exists("User",
#                                                   email) or username is not None and frappe.db.exists("User", {'username': username}):
#         if frappe.db.exists("Role", role):
#             set_user_permissions(context, username, email, role)
#         else:
#             print("Role does not exist")


@click.command('set-user-permissions')
@click.option('--username')
@click.option('--email')
@click.option('--role')
@pass_context
def set_user_permissions(context, username=None, email=None, role=None):
    """
    Set user permissions for site
    :return:
    """
    site = context.obj['sites'][0]
    frappe.init(site=site)
    frappe.connect(site)
    if username is not None:
        user = frappe.get_doc("User", {'username': username})
        user.add_roles(role)
    if email is not None:
        add_role(email, role)

@click.command('list-users')
@pass_context
def list_users(context):
    site = context.obj['sites'][0]
    frappe.init(site=site)
    frappe.connect(site)
    users = frappe.get_all("User")
    for user in users:
        print(user.name)

commands = [set_user_permissions, list_users]



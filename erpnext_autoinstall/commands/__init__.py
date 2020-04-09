from __future__ import unicode_literals, absolute_import
import click
import frappe
from click import pass_context
from frappe.utils.user import add_role


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
    user = None
    frappe.connect(site)
    if username is not None:
        add_role(username, role)
    if email is not None:
        add_role(email, role)



commands = [set_user_permissions]

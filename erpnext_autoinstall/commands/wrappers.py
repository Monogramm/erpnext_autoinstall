import sys

import frappe


def connect_to_db_wrapper(f):
    def accept_arguments(context, **kwargs):
        site = context.obj['sites'][0]
        frappe.init(site=site)
        frappe.connect(site)
        f(**kwargs)

    return accept_arguments


def is_email_exists_wrapper(f):
    def accept_arguments(kwargs):
        if not frappe.get_all("User", filters={'email': kwargs['email']}):
            print("Error: Email {} does not exist".format(kwargs['email']))
            sys.exit(1)
        f(kwargs)

    return accept_arguments


def is_username_exists_wrapper(f):
    def accept_arguments(kwargs):
        if not frappe.db.exists('User', {'username': kwargs['username']}):
            print("Error: Username {} does not exist".format(kwargs['username']))
            sys.exit(1)
        f(kwargs)

    return accept_arguments


def is_roles_exist_wrapper(f):
    def accept_arguments(kwargs):
        for role in kwargs['roles']:
            if not frappe.db.exists('Role', role):
                print("Error: Role {} does not exist".format(role))
                sys.exit(1)

    return accept_arguments


@is_email_exists_wrapper
@is_username_exists_wrapper
@is_roles_exist_wrapper
def _checker(username, email, roles):
    print("Username {} ".format(username))
    print("Email {}".format(email))
    print("Roles {}".format(roles))
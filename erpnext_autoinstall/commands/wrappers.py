import sys

import frappe


def connect_to_db(f):
    def accept_arguments(context, **kwargs):
        site = context.obj['sites'][0]
        frappe.init(site=site)
        frappe.connect(site)
        try:
            f(**kwargs)
        finally:
            frappe.destroy()

    return accept_arguments


def email_exists(f):
    """Wrapper on function f. This function check, that email exists."""
    def accept_arguments(**kwargs):
        if not frappe.get_all("User", filters=[{'email': kwargs['email']}]):
            print("Error: Email {} does not exist".format(kwargs['email']))
            sys.exit(1)
        f(**kwargs)

    return accept_arguments


def username_exists(f):
    """Wrapper on function f. This function check, that username exists."""
    def accept_arguments(**kwargs):
        if not frappe.db.exists('User', {'username': kwargs['username']}):
            print("Error: Username {} does not exist".format(kwargs['username']))
            sys.exit(1)
        f(**kwargs)

    return accept_arguments


def roles_exist(f):
    """Wrapper on function f. This function check, that roles exists."""
    def accept_arguments(**kwargs):
        for role in kwargs['roles']:
            if not frappe.db.exists('Role', role):
                print(frappe.get_all("Role"))
                print("Error: Permission {} does not exist".format(role))
                sys.exit(1)
        f(**kwargs)
    return accept_arguments


def role_profile_exists(f):
    """Wrapper on function f. This function check, that role profile exists."""
    def accept_arguments(**kwargs):
        if not frappe.db.exists("Role Profile", kwargs['role']):
            print("Error: Role {} does not exist".format(kwargs['role']))
            sys.exit(1)
        f(**kwargs)

    return accept_arguments


@email_exists
@username_exists
@roles_exist
def _checker(username, email, roles):
    print("Username {} ".format(username))
    print("Email {}".format(email))
    print("Roles {}".format(roles))
    return username, email, roles

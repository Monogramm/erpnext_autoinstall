import sys

import frappe


def connect_to_db_wrapper(f):
    def accept_arguments(context, **args):
        site = context.obj['sites'][0]
        frappe.init(site=site)
        frappe.connect(site)
        f(**args)

    return accept_arguments


def is_email_exists_wrapper(f):
    def accept_arguments(**args):
        if not frappe.db.exists('User', args['email']):
            print("Error: Email {} does not exist".format(args['email']))
            sys.exit(1)
        f(**args)

    return accept_arguments


def is_username_exists_wrapper(f):
    def accept_arguments(**args):
        if not frappe.db.exists('User', {'username': args['username']}):
            print("Error: Username {} does not exist".format(args['username']))
            sys.exit(1)
        f(**args)

    return accept_arguments


def is_roles_exist_wrapper(f):
    def accept_arguments(**args):
        for role in args['roles']:
            if not frappe.db.exists('Role', role):
                print("Error: Role {} does not exist".format(role))
                sys.exit(1)

    return accept_arguments

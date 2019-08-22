import os

import frappe


def configure_app():
    disable_registration()
    configure_email()
    make_configuration()



def configure_email():
    email_account = frappe.get_doc("Email Domain", "example.com")
    email_account.email_server = os.getenv('Example Email Address')
    email_account.email_id = os.getenv('Example Email Address')
    email_account.domain_name = os.getenv('Domain Name')
    email_account.smtp_server = os.getenv('SMTP Server')
    email_account.smtp_port = int(os.getenv('Port'))
    email_account.use_imap = int(os.getenv('Use IMAP'))
    email_account.use_ssl = int(os.getenv('Use SSL'))
    email_account.tls = int(os.getenv('Use TLS'))
    email_account.attachment_limit = int(os.getenv('Attachment Limit (MB)'))
    email_account.save()



def make_configuration():
    doc = frappe.get_doc("LDAP Settings")
    doc.ldap_email_field = os.getenv('LDAP Email Field')
    doc.base_dn = os.getenv('Base Distinguished Name (DN)')
    doc.ldap_first_name_field = os.getenv('LDAP First Name Field')
    doc.ldap_search_string = os.getenv('LDAP Search String')
    doc.ldap_server_url = os.getenv('LDAP Server Url')
    doc.default_role = os.getenv('Default Role on Creation')
    doc.ldap_username_field = os.getenv('LDAP Username Field')
    doc.organizational_unit = os.getenv('Organizational Unit for Users')
    doc.password = os.getenv('Password for Base DN')
    doc.save()


def disable_registration():
    doc = frappe.get_doc("Website Settings")
    doc.disable_signup = 0
    doc.save()

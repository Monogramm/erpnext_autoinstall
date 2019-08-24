import os

import frappe


def configure_app():
    disable_registration()
    configure_email()
    configure_LDAP()


def configure_domain():
    email_account = frappe.new_doc("Email Domain")
    email_account.email_server = os.getenv('EMAIL_SERVER')
    #email_account.email_id = os.getenv('EMAIL_ADDRESS')
    email_account.domain_name = os.getenv('EMAIL_DOMAIN_NAME')
    email_account.smtp_server = os.getenv('EMAIL_SMTP_SERVER')
    email_account.smtp_port = int(os.getenv('EMAIL_PORT'))
    email_account.use_imap = int(os.getenv('EMAIL_USE_IMAP'))
    email_account.use_ssl = int(os.getenv('EMAIL_USE_SSL'))
    email_account.tls = int(os.getenv('EMAIL_USE_TLS'))
    email_account.attachment_limit = int(os.getenv('EMAIL_ATTACHMENT_LIMIT_MB'))
    email_account.save()

def configure_account():
    email_account = frappe.new_doc("Email Account")
    email_account.email_account_name = os.getenv("EMAIL_ADDRESS")
    email_account.password = os.getenv("EMAIL_PASSWORD")
    email_account.domain = os.getenv("EMAIL_DOMAIN")
    email_account.save()

def configure_email():
    configure_domain()
    configure_account()

def configure_LDAP():
    doc = frappe.get_doc("LDAP_SETTINGS")
    doc.ldap_email_field = os.getenv('LDAP_EMAIL')
    doc.base_dn = os.getenv('LDAP_BASE_DISTINGUISHED_NAME')
    doc.ldap_first_name_field = os.getenv('LDAP_FIRST_NAME')
    doc.ldap_search_string = os.getenv('LDAP_SEARCH_STRING')
    doc.ldap_server_url = os.getenv('LDAP_SERVER_URL')
    doc.default_role = os.getenv('LDAP_DEFAULT_ROLE_ON_CREATION')
    doc.ldap_username_field = os.getenv('LDAP_USERNAME')
    doc.organizational_unit = os.getenv('LDAP_Organizational_UNIT_FOR_USERS')
    doc.password = os.getenv('LDAP_Password_FOR_BASE_DN')
    doc.save()


def disable_registration():
    doc = frappe.get_doc("Website Settings")
    doc.disable_signup = int(os.getenv('DISABLE_SIGNUP'))
    doc.save()

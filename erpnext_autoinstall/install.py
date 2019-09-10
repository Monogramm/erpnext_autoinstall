import os

import frappe


def after_install():
    disable_registration()
    # TODO Only if EMAIL_SERVER define
    configure_email()
    # TODO Only if LDAP_SERVER_URL define
    configure_ldap()


def disable_registration():
    doc = frappe.get_doc("Website Settings")
    doc.disable_signup = int(os.getenv('DISABLE_SIGNUP', '0'))
    doc.save()


def configure_domain():
    email_domain = frappe.new_doc("Email Domain")
    email_domain.email_server = os.getenv('EMAIL_SERVER')
    email_domain.email_id = os.getenv('EMAIL_ADDRESS')
    email_domain.domain_name = os.getenv('EMAIL_DOMAIN_NAME')
    email_domain.smtp_server = os.getenv('EMAIL_SMTP_SERVER')
    email_domain.smtp_port = int(os.getenv('EMAIL_PORT'))
    email_domain.use_imap = int(os.getenv('EMAIL_USE_IMAP'))
    email_domain.use_ssl = int(os.getenv('EMAIL_USE_SSL'))
    email_domain.tls = int(os.getenv('EMAIL_USE_TLS'))
    email_domain.attachment_limit = int(os.getenv('EMAIL_ATTACHMENT_LIMIT_MB'))
    email_domain.save()

def configure_account():
    email_account = frappe.new_doc("Email Account")
    email_account.email_account_name = os.getenv("EMAIL_ADDRESS")
    email_account.password = os.getenv("EMAIL_PASSWORD")
    email_account.domain = os.getenv("EMAIL_DOMAIN")
    email_account.save()

def configure_email():
    configure_domain()
    configure_account()
    # TODO Update Admin email address


def configure_ldap():
    doc = frappe.get_doc("LDAP Settings")

    doc.ldap_server_url = os.getenv('LDAP_SERVER_URL')
    doc.base_dn = os.getenv('LDAP_BASE_DN')
    doc.password = os.getenv('LDAP_PASSWORD')

    doc.organizational_unit = os.getenv('LDAP_USERS_ORGANIZATIONAL_UNIT')
    doc.default_role = os.getenv('LDAP_DEFAULT_ROLE', 'Employee')
    doc.ldap_search_string = os.getenv('LDAP_SEARCH_STRING', 'uid=\{0\}')

    doc.ldap_email_field = os.getenv('LDAP_EMAIL', 'mail')
    doc.ldap_username_field = os.getenv('LDAP_USERNAME', 'uid')
    doc.ldap_first_name_field = os.getenv('LDAP_FIRST_NAME', 'givenName')
    doc.ldap_last_name_field = os.getenv('LDAP_LAST_NAME', 'sn')
    doc.ldap_phone_field = os.getenv('LDAP_PHONE_FIELD', 'telephoneNumber')
    doc.ldap_mobile_field = os.getenv('LDAP_MOBILE_FIELD', 'mobile')

    doc.ssl_tls_mode = os.getenv('LDAP_SSL_TLS_MODE')

    # TODO Enable LDAP Settings

    doc.save()

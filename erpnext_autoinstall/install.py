import os

import frappe


def after_install():
    disable_registration()
    configure_email()
    configure_ldap()


def disable_registration():
    doc = frappe.get_doc("Website Settings")
    doc.disable_signup = int(os.getenv('DISABLE_SIGNUP', '0'))
    doc.save()
    print("REGISTRATION HAS BEEN CONFIGURED!")


def configure_domain():
    if os.getenv('EMAIL SERVER') and os.getenv('EMAIL_DOMAIN_ID') and os.getenv('EMAIL_DOMAIN_NAME') and os.getenv(
            'EMAIL_DOMAIN_SMTP_SERVER') and os.getenv('EMAIL_DOMAIN_USE_IMAP') and os.getenv('EMAIL_DOMAIN_ATTACHMENT_LIMIT_MB'):
        email_domain = frappe.new_doc("Email Domain")
        email_domain.email_server = os.getenv('EMAIL_DOMAIN_SERVER')
        email_domain.email_id = os.getenv('EMAIL_DOMAIN_ID')
        email_domain.domain_name = os.getenv('EMAIL_DOMAIN_NAME')
        email_domain.smtp_server = os.getenv('EMAIL_DOMAIN_SMTP_SERVER')
        email_domain.smtp_port = int(os.getenv('EMAIL_DOMAIN_PORT', '993'))
        email_domain.use_imap = int(os.getenv('EMAIL_DOMAIN_USE_IMAP'))
        email_domain.use_ssl = int(os.getenv('EMAIL_DOMAIN_USE_SSL', '1'))
        email_domain.tls = int(os.getenv('EMAIL_DOMAIN_USE_TLS', '0'))
        email_domain.attachment_limit = int(os.getenv('EMAIL_DOMAIN_ATTACHMENT_LIMIT_MB'))
        email_domain.save()
        print("EMAIL DOMAIN HAS BEEN CONFIGURED!")


def configure_account():
    email_account = frappe.new_doc("Email Account")
    email_account.email_account_name = os.getenv("EMAIL_ACCOUNT_ADDRESS_ACCOUNT")
    email_account.password = os.getenv("EMAIL_ACCOUNT_PASSWORD")
    email_account.domain = os.getenv("EMAIL_DOMAIN_NAME")
    email_account.save()
    print("EMAIL ACCOUNT(S) HAS BEEN CONFIGURED!")


def configure_email():
    configure_domain()
    # TODO: Rework email account(s) configuration
    #configure_account()
    # TODO: Add a user account(s) update


# Todo: maybe should remade as @decorator
def configure_ldap():
    if os.getenv('LDAP_SERVER_URL') and os.getenv('LDAP_BASE_DN') and os.getenv('LDAP_PASSWORD') and os.getenv(
            'LDAP_USERS_ORGANIZATIONAL_UNIT') and os.getenv('LDAP_SSL_TLS_MODE'):
        doc = frappe.get_doc("LDAP Settings")

        doc.ldap_server_url = os.getenv('LDAP_SERVER_URL')
        doc.base_dn = os.getenv('LDAP_BASE_DN')
        doc.password = os.getenv('LDAP_PASSWORD')

        doc.organizational_unit = os.getenv('LDAP_USERS_ORGANIZATIONAL_UNIT')
        doc.default_role = os.getenv('LDAP_DEFAULT_ROLE', 'Employee')
        doc.ldap_search_string = os.getenv('LDAP_SEARCH_STRING', 'uid=\{0\}')

        doc.ldap_email_field = os.getenv('LDAP_EMAIL_FIELD', 'mail')
        doc.ldap_username_field = os.getenv('LDAP_USERNAME_FIELD', 'uid')
        doc.ldap_first_name_field = os.getenv('LDAP_FIRST_NAME_FIELD', 'givenName')
        doc.ldap_middle_name_field = os.getenv('LDAP_MIDDLE_NAME_FIELD', '')
        doc.ldap_last_name_field = os.getenv('LDAP_LAST_NAME_FIELD', 'sn')
        doc.ldap_phone_field = os.getenv('LDAP_PHONE_FIELD', 'telephoneNumber')
        doc.ldap_mobile_field = os.getenv('LDAP_MOBILE_FIELD', 'mobile')

        doc.ssl_tls_mode = os.getenv('LDAP_SSL_TLS_MODE')
        doc.enabled = int(os.getenv('LDAP_ENABLED', '1'))

        doc.save()
        print("LDAP HAS BEEN CONFIGURED!")
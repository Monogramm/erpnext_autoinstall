import os

import frappe


def configure_app():
    configure_email()
    make_configuration()



def configure_email():
    configure_info = get_configuration_from_file("/home/emil/Desktop/frappe-bench/apps/erpnext_autoinstall/configuration/email_config.txt")
    email_account = frappe.get_doc("Email Domain", "example.com")
    email_account.email_server = configure_info['Example Email Address']
    email_account.email_id = configure_info['Example Email Address']
    email_account.domain_name = configure_info['Example Email Address'].split('@')[1]
    email_account.smtp_server = configure_info.get('SMTP Server')
    email_account.smtp_port = int(configure_info.get('Port'))
    email_account.use_imap = int(configure_info.get('Use IMAP'))
    email_account.use_ssl = int(configure_info.get('Use SSL'))
    email_account.tls = int(configure_info.get('Use TLS'))
    email_account.attachment_limit = int(configure_info.get('Attachment Limit (MB)'))
    email_account.save()

def get_configuration_from_file(file_name):
    dict_with_info = {}
    print("Taking configuration from file: "+str(file_name))
    with open(file_name) as config_file:
        for line in config_file:
            dict_with_info[line.split(':')[0]] = line.split(':')[1].replace("\n",'')
    print(dict_with_info)
    return dict_with_info


def make_configuration():
    configuration_dict = get_configuration_from_file("/home/emil/Desktop/frappe-bench/apps/erpnext_autoinstall/configuration/configuration_file.txt")
    doc = frappe.get_doc("LDAP Settings")
    doc.ldap_email_field = configuration_dict['LDAP Email Field']
    doc.base_dn = configuration_dict['Base Distinguished Name (DN)']
    doc.ldap_first_name_field = configuration_dict['LDAP First Name Field']
    doc.ldap_search_string = configuration_dict['LDAP Search String']
    doc.ldap_server_url = configuration_dict['LDAP Server Url']
    doc.default_role = configuration_dict['Default Role on Creation']
    doc.ldap_username_field = configuration_dict['LDAP Username Field']
    doc.organizational_unit = configuration_dict['Organizational Unit for Users']
    doc.password = configuration_dict['Password for Base DN']
    doc.save()

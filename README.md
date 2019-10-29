
[uri_license]: http://www.gnu.org/licenses/agpl.html
[uri_license_image]: https://img.shields.io/badge/License-AGPL%20v3-blue.svg
[![Build Status](https://travis-ci.org/Monogramm/erpnext_autoinstall.svg)](https://travis-ci.org/Monogramm/erpnext_autoinstall)

[![License: AGPL v3][uri_license_image]][uri_license]

## ERPNext AutoInstall

:alembic: **Experimental** ERPNext application for automatic setup.

The objective is to setup ERPNext automatically based on environment variables, mainly for docker usage.

#### License

AGPL

## Installation

  ```
  bench get-app --branch develop erpnext_autoinstall https://github.com/Monogramm/erpnext_autoinstall
  bench install-app erpnext_autoinstall
  ```

## How to use

Environment variables for automatic setup:
* WebSite configuration
  * DISABLE_SIGNUP
* Email configuration
  * EMAIL_SERVER
  * EMAIL_ADDRESS
  * EMAIL_DOMAIN_NAME
  * EMAIL_SMTP_SERVER
  * EMAIL_PORT
  * EMAIL_USE_IMAP
  * EMAIL_USE_SSL
  * EMAIL_USE_TLS
  * EMAIL_ATTACHMENT_LIMIT_MB
  * EMAIL_PASSWORD
* LDAP configuration
  * LDAP_SERVER_URL
  * LDAP_BASE_DN
  * LDAP_PASSWORD
  * LDAP_USERS_ORGANIZATIONAL_UNIT
  * LDAP_DEFAULT_ROLE
  * LDAP_SEARCH_STRING
  * LDAP_EMAIL
  * LDAP_USERNAME
  * LDAP_FIRST_NAME
  * LDAP_LAST_NAME
  * LDAP_PHONE_FIELD
  * LDAP_MOBILE_FIELD
  * LDAP_SSL_TLS_MODE
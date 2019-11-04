
[uri_license]: http://www.gnu.org/licenses/agpl.html
[uri_license_image]: https://img.shields.io/badge/License-AGPL%20v3-blue.svg

[![License: AGPL v3][uri_license_image]][uri_license]
[![Managed with Taiga.io](https://img.shields.io/badge/managed%20with-TAIGA.io-709f14.svg)](https://tree.taiga.io/project/monogrammbot-monogrammerpnext_autoinstall/ "Managed with Taiga.io")
[![Build Status](https://travis-ci.org/Monogramm/erpnext_autoinstall.svg)](https://travis-ci.org/Monogramm/erpnext_autoinstall)

## ERPNext AutoInstall

:alembic: **Experimental** Frappe application for automatic setup of ERPNext.

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
  * `DISABLE_SIGNUP`
* Email domain configuration
  * `EMAIL_DOMAIN_SERVER`
  * `EMAIL_DOMAIN_ID`
  * `EMAIL_DOMAIN_NAME`
  * `EMAIL_DOMAIN_SMTP_SERVER`
  * `EMAIL_DOMAIN_PORT`
  * `EMAIL_DOMAIN_USE_IMAP`
  * `EMAIL_DOMAIN_USE_SSL`
  * `EMAIL_DOMAIN_USE_TLS`
  * `EMAIL_DOMAIN_ATTACHMENT_LIMIT_MB`
* Email accounts configuration (WIP)
  * `EMAIL_ACCOUNT_ADDRESS_ACCOUNT`
  * `EMAIL_ACCOUNT_PASSWORD`
* LDAP configuration
  * `LDAP_ENABLED`
  * `LDAP_SERVER_URL`
  * `LDAP_BASE_DN`
  * `LDAP_PASSWORD`
  * `LDAP_USERS_ORGANIZATIONAL_UNIT`
  * `LDAP_DEFAULT_ROLE`
  * `LDAP_SEARCH_STRING`
  * `LDAP_EMAIL_FIELD`
  * `LDAP_USERNAME_FIELD`
  * `LDAP_FIRST_NAME_FIELD`
  * `LDAP_MIDDLE_NAME_FIELD`
  * `LDAP_LAST_NAME_FIELD`
  * `LDAP_PHONE_FIELD`
  * `LDAP_MOBILE_FIELD`
  * `LDAP_SSL_TLS_MODE`
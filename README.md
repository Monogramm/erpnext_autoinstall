
[uri_license]: http://www.gnu.org/licenses/agpl.html
[uri_license_image]: https://img.shields.io/badge/License-AGPL%20v3-blue.svg

[![License: AGPL v3][uri_license_image]][uri_license]
[![Managed with Taiga.io](https://img.shields.io/badge/managed%20with-TAIGA.io-709f14.svg)](https://tree.taiga.io/project/monogrammbot-monogrammerpnext_autoinstall/ "Managed with Taiga.io")
[![Build Status](https://travis-ci.org/Monogramm/erpnext_autoinstall.svg)](https://travis-ci.org/Monogramm/erpnext_autoinstall)
[![Coverage Status](https://coveralls.io/repos/github/Monogramm/erpnext_autoinstall/badge.svg?branch=master)](https://coveralls.io/github/Monogramm/erpnext_autoinstall?branch=master)

# ERPNext AutoInstall

> :alembic: **Experimental** Frappe application for automatic setup of ERPNext.

The objective is to setup ERPNext automatically based on environment variables, mainly for docker usage.

https://discuss.erpnext.com/t/setup-ldap-through-command-line/49735

## :construction: Install

```sh
bench get-app --branch master erpnext_autoinstall https://github.com/Monogramm/erpnext_autoinstall
```

## :rocket: Usage

```sh
bench install-app erpnext_autoinstall
```

Environment variables for automatic setup:
* WebSite configuration
  * `DISABLE_SIGNUP`
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
  
Environment variables **not ready yet**:
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
* Email accounts configuration
  * `EMAIL_ACCOUNT_ADDRESS_ACCOUNT`
  * `EMAIL_ACCOUNT_PASSWORD`

## :white_check_mark: Run tests

```sh
bench bench run-tests --profile --app erpnext_autoinstall
```

## :bust_in_silhouette: Authors

**Monogramm**

* Website: https://www.monogramm.io
* Github: [@Monogramm](https://github.com/Monogramm)

**Аминов Эмиль**

* Website: https://aminove99.github.io/
* Github: [@AminovE99](https://github.com/AminovE99)

## :handshake: Contributing

Contributions, issues and feature requests are welcome!<br />Feel free to check [issues page](https://github.com/Monogramm/erpnext_autoinstall/issues).
[Check the contributing guide](./CONTRIBUTING.md).<br />

## :thumbsup: Show your support

Give a :star: if this project helped you!

## :page_facing_up: License

Copyright © 2019 [Monogramm](https://github.com/Monogramm).<br />
This project is [AGPL v3](uri_license) licensed.

***
_This README was generated with :heart: by [readme-md-generator](https://github.com/kefranabg/readme-md-generator)_

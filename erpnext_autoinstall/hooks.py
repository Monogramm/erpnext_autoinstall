# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import __version__ as app_version

app_name = "erpnext_autoinstall"
app_title = "ERPNext AutoInstall"
app_publisher = "Monogramm"
app_description = "Frappe application to automatically setup ERPNext through environment variables."
app_icon = "octicon octicon-circuit-board"
app_color = "#252525"
app_email = "opensource@monogramm.io"
app_license = "AGPLv3"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/erpnext_autoinstall/css/erpnext_autoinstall.css"
# app_include_js = "/assets/erpnext_autoinstall/js/erpnext_autoinstall.js"

# include js, css files in header of web template
# web_include_css = "/assets/erpnext_autoinstall/css/erpnext_autoinstall.css"
# web_include_js = "/assets/erpnext_autoinstall/js/erpnext_autoinstall.js"

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Website user home page (by function)
# get_website_user_home_page = "erpnext_autoinstall.utils.get_home_page"

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "erpnext_autoinstall.install.before_install"
after_install = "erpnext_autoinstall.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "erpnext_autoinstall.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
#	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"erpnext_autoinstall.tasks.all"
# 	],
# 	"daily": [
# 		"erpnext_autoinstall.tasks.daily"
# 	],
# 	"hourly": [
# 		"erpnext_autoinstall.tasks.hourly"
# 	],
# 	"weekly": [
# 		"erpnext_autoinstall.tasks.weekly"
# 	]
# 	"monthly": [
# 		"erpnext_autoinstall.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "erpnext_autoinstall.install.before_tests"

# Overriding Whitelisted Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "erpnext_autoinstall.event.get_events"
# }


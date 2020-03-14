# -*- coding: utf-8 -*-
# Copyright (c) 2020, Monogramm and Contributors
# See license.txt
"""
Configuration for desktop.
"""

from __future__ import unicode_literals

from frappe import _


def get_data():
	return [
		{
			"module_name": "ERPNext AutoInstall",
			"color": "#252525",
			"icon": "octicon octicon-circuit-board",
			"type": "module",
			"label": _("ERPNext AutoInstall")
		}
	]

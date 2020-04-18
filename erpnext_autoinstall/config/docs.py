# -*- coding: utf-8 -*-
# Copyright (c) 2020, Monogramm and Contributors
# See license.txt
"""Configuration for docs."""

from __future__ import unicode_literals


source_link = "https://github.com/Monogramm/erpnext_autoinstall"
docs_base_url = "https://monogramm.github.io/erpnext_autoinstall"
headline = "TODO_APP_DESCRIPTION"
sub_heading = "TODO_APP_USAGE"


def get_context(context):
    context.brand_html = "ERPNext AutoInstall"
    context.source_link = source_link
    context.docs_base_url = docs_base_url
    context.headline = headline
    context.sub_heading = sub_heading

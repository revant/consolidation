# -*- coding: utf-8 -*-
from __future__ import unicode_literals

app_name = "consolidation"
app_title = "Consolidation"
app_publisher = "Revant Nandgaonkar"
app_description = "Frappe / ERPNext app for Consolidation"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "revant.one@gmail.com"
app_version = "0.0.1"
app_license = "GPL v3"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/consolidation/css/consolidation.css"
# app_include_js = "/assets/consolidation/js/consolidation.js"

# include js, css files in header of web template
# web_include_css = "/assets/consolidation/css/consolidation.css"
# web_include_js = "/assets/consolidation/js/consolidation.js"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Website user home page (by function)
# get_website_user_home_page = "consolidation.utils.get_home_page"

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "consolidation.install.before_install"
# after_install = "consolidation.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "consolidation.notifications.get_notification_config"

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
# 		"consolidation.tasks.all"
# 	],
# 	"daily": [
# 		"consolidation.tasks.daily"
# 	],
# 	"hourly": [
# 		"consolidation.tasks.hourly"
# 	],
# 	"weekly": [
# 		"consolidation.tasks.weekly"
# 	]
# 	"monthly": [
# 		"consolidation.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "consolidation.install.before_tests"

# Overriding Whitelisted Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "consolidation.event.get_events"
# }


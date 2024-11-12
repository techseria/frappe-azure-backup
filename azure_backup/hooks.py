from . import __version__ as app_version

app_name = "azure_backup"
app_title = "Azure Backup"
app_publisher = "Techseria"
app_description = "Take daily site backup into Azure Blob Storage"
app_email = "support@techseria.com"
app_license = "agpl-3.0"
app_icon = "octicon octicon-cloud-upload"
app_color = "blue"

# Apps
# ------------------

# required_apps = []

# Each item in the list will be shown as an app in the apps page
# add_to_apps_screen = [
# 	{
# 		"name": "azure_backup",
# 		"logo": "/assets/azure_backup/logo.png",
# 		"title": "Azure Backup",
# 		"route": "/azure_backup",
# 		"has_permission": "azure_backup.api.permission.has_app_permission"
# 	}
# ]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/azure_backup/css/azure_backup.css"
# app_include_js = "/assets/azure_backup/js/azure_backup.js"

# include js, css files in header of web template
# web_include_css = "/assets/azure_backup/css/azure_backup.css"
# web_include_js = "/assets/azure_backup/js/azure_backup.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "azure_backup/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "azure_backup/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
home_page = "azure_backup_home"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "azure_backup.utils.jinja_methods",
# 	"filters": "azure_backup.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "azure_backup.install.before_install"
# after_install = "azure_backup.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "azure_backup.uninstall.before_uninstall"
# after_uninstall = "azure_backup.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "azure_backup.utils.before_app_install"
# after_app_install = "azure_backup.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "azure_backup.utils.before_app_uninstall"
# after_app_uninstall = "azure_backup.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "azure_backup.notifications.get_notification_config"

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

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
    "Azure Backup Settings": {
        "on_update": "azure_backup.tasks.update_backup_schedule"
    }
	# "*": {
	# 	"on_update": "method",
	# 	"on_cancel": "method",
	# 	"on_trash": "method"
	# }
}

# import frappe
# from datetime import datetime

# def get_backup_time():
#     settings = frappe.get_single("Azure Backup Settings")
#     if not settings.backup_time:
#         frappe.logger().warn("No backup time set in Azure Backup Settings.")
#         return None

#     return datetime.strptime(settings.backup_time, '%H:%M:%S').time()

# def schedule_backup():
#     print("test")
#     backup_time = get_backup_time()
#     if backup_time:
#         cron_expression = f"{backup_time.minute} {backup_time.hour} * * *"
#         return cron_expression
#     return None

# backup_cron = schedule_backup()
# print(backup_cron)

# scheduler_events = {
#     "cron": {
#         "39 16 * * *": [
#             "azure_backup.tasks.upload_backup_to_azure"
#         ]
#     }
# }
    

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	# "all": [
# 	# 	"azure_backup.tasks.all"
# 	# ],
    
# 	# "daily": [
# 	# 	"azure_backup.tasks.upload_backup_to_azure"
# 	# ],
# # 	"hourly": [
# # 		"azure_backup.tasks.hourly"
# # 	],
# # 	"weekly": [
# # 		"azure_backup.tasks.weekly"
# # 	],
# # 	"monthly": [
# # 		"azure_backup.tasks.monthly"
# # 	],
# }

# Testing
# -------

# before_tests = "azure_backup.install.before_tests"

# Overriding Methods
# ------------------------------
#
override_whitelisted_methods = {
	# "frappe.desk.doctype.event.event.get_events": "azure_backup.event.get_events"
}
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "azure_backup.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["azure_backup.utils.before_request"]
# after_request = ["azure_backup.utils.after_request"]

# Job Events
# ----------
# before_job = ["azure_backup.utils.before_job"]
# after_job = ["azure_backup.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"azure_backup.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }

fixtures = ["Azure Backup Settings"]
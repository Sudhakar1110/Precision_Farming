app_name = "agri_connect"
app_title = "Agri Connect"
app_publisher = "Bizaxl"
app_description = "Weather and IOT connectors for agrilculture module"
app_email = "admin@bizaxl.com"
app_license = "mit"

# Apps
# ------------------

required_apps = ["frappe", "erpnext", "agriculture"]

# Fixtures
# --------

fixtures = [
	"Server Script",
	"Client Script",
	{"dt": "Custom Field", "filters": [["module", "=", "Agri Connect"]]},
	{"dt": "Report", "filters": [["module", "=", "Agri Connect"]]},
	{"dt": "Number Card", "filters": [["module", "=", "Agri Connect"]]},
	{"dt": "Role", "filters": [["name", "in", ["Agriculture Manager", "Agriculture User"]]]},
	{"dt": "Role Profile", "filters": [["name", "in", ["Farm Manager", "Field Officer"]]]},
	"Waste Category",
	"Waste Type",
	"Application Method",
	"Compost Quality Parameter",
	"Crop Nutrient Standard",
	"Fertilizer Product",
	"Soil Nutrient Threshold",
]

# Each item in the list will be shown as an app in the apps page
# add_to_apps_screen = [
# 	{
# 		"name": "agri_connect",
# 		"logo": "/assets/agri_connect/logo.png",
# 		"title": "Agri Connect",
# 		"route": "/agri_connect",
# 		"has_permission": "agri_connect.api.permission.has_app_permission"
# 	}
# ]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/agri_connect/css/agri_connect.css"
# app_include_js = "/assets/agri_connect/js/agri_connect.js"

# include js, css files in header of web template
# web_include_css = "/assets/agri_connect/css/agri_connect.css"
# web_include_js = "/assets/agri_connect/js/agri_connect.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "agri_connect/public/scss/website"

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
# app_include_icons = "agri_connect/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

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
# 	"methods": "agri_connect.utils.jinja_methods",
# 	"filters": "agri_connect.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "agri_connect.install.before_install"
after_install = "agri_connect.install.after_install"
after_migrate = "agri_connect.install.after_migrate"

# Uninstallation
# ------------

# before_uninstall = "agri_connect.uninstall.before_uninstall"
# after_uninstall = "agri_connect.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "agri_connect.utils.before_app_install"
# after_app_install = "agri_connect.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "agri_connect.utils.before_app_uninstall"
# after_app_uninstall = "agri_connect.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "agri_connect.notifications.get_notification_config"

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
	"Waste Record": {
		"validate": "agri_connect.agri_connect.doctype.waste_record.waste_record.validate",
		"on_submit": "agri_connect.agri_connect.doctype.waste_record.waste_record.on_submit",
		"on_cancel": "agri_connect.agri_connect.doctype.waste_record.waste_record.on_cancel"
	},
	"Composting Batch": {
		"validate": "agri_connect.agri_connect.doctype.composting_batch.composting_batch.validate",
		"on_submit": "agri_connect.agri_connect.doctype.composting_batch.composting_batch.on_submit",
		"on_cancel": "agri_connect.agri_connect.doctype.composting_batch.composting_batch.on_cancel"
	},
	"Compost Quality Check": {
		"validate": "agri_connect.agri_connect.doctype.compost_quality_check.compost_quality_check.validate",
		"on_submit": "agri_connect.agri_connect.doctype.compost_quality_check.compost_quality_check.on_submit"
	},
	"Compost Application": {
		"validate": "agri_connect.agri_connect.doctype.compost_application.compost_application.validate",
		"on_submit": "agri_connect.agri_connect.doctype.compost_application.compost_application.on_submit",
		"on_cancel": "agri_connect.agri_connect.doctype.compost_application.compost_application.on_cancel"
	},
	"Soil Analysis": {
		"validate": "agri_connect.agri_connect.doctype.soil_analysis.soil_analysis.validate"
	},
	"Nutrient Analysis": {
		"validate": "agri_connect.agri_connect.doctype.nutrient_analysis.nutrient_analysis.validate"
	},
	"Fertilizer Recommendation": {
		"validate": "agri_connect.agri_connect.doctype.fertilizer_recommendation.fertilizer_recommendation.validate",
		"on_submit": "agri_connect.agri_connect.doctype.fertilizer_recommendation.fertilizer_recommendation.on_submit",
		"on_update_after_submit": "agri_connect.agri_connect.doctype.fertilizer_recommendation.fertilizer_recommendation.on_update_after_submit"
	},
	"Fertilizer Application": {
		"validate": "agri_connect.agri_connect.doctype.fertilizer_application.fertilizer_application.validate",
		"on_submit": "agri_connect.agri_connect.doctype.fertilizer_application.fertilizer_application.on_submit",
		"on_cancel": "agri_connect.agri_connect.doctype.fertilizer_application.fertilizer_application.on_cancel"
	},
	"Recycling Record": {
		"on_submit": "agri_connect.agri_connect.doctype.recycling_record.recycling_record.on_submit"
	},
	"Disposal Record": {
		"on_submit": "agri_connect.agri_connect.doctype.disposal_record.disposal_record.on_submit"
	}
}

# Scheduled Tasks
# ---------------

scheduler_events = {
	"daily": [
		"agri_connect.api.update_weather_daily",
		"agri_connect.agri_connect.tasks.check_compliance_expiry",
		"agri_connect.agri_connect.tasks.send_application_reminders"
	],
	"weekly": [
		"agri_connect.agri_connect.tasks.generate_waste_summary",
		"agri_connect.agri_connect.tasks.generate_fertilizer_report"
	],
	"monthly": [
		"agri_connect.agri_connect.tasks.generate_nutrient_balance_report"
	],
}

# Testing
# -------

# before_tests = "agri_connect.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "agri_connect.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "agri_connect.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["agri_connect.utils.before_request"]
# after_request = ["agri_connect.utils.after_request"]

# Job Events
# ----------
# before_job = ["agri_connect.utils.before_job"]
# after_job = ["agri_connect.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,# },

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"agri_connect.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }

# Translation
# ------------
# List of apps whose translatable strings should be excluded from this app's translations.
# ignore_translatable_strings_from = []


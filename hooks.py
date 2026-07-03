app_name = "Precision_Farming"
app_title = "Precision Farming"
app_publisher = "Precision Farming Solutions"
app_description = "Waste Management and Fertilizer Measurement for Precision Farming"
app_email = "admin@precisionfarming.com"
app_license = "mit"

# Apps
# ------------------

required_apps = ["frappe", "erpnext"]

# Fixtures
# --------

# Installation
# ------------

after_install = "Precision_Farming.install.after_install"
after_migrate = "Precision_Farming.install.after_migrate"

# Fixtures
# --------

fixtures = [
	"Waste Category",
	"Waste Type",
	"Application Method",
	"Compost Quality Parameter",
	"Crop Nutrient Standard",
	"Fertilizer Product",
	"Soil Nutrient Threshold",
	{"dt": "Workspace", "filters": [["name", "=", "Precision Farming"]]},
]

# Scheduled Tasks
# ---------------

scheduler_events = {
	"daily": [
		"Precision_Farming.tasks.check_compliance_expiry",
		"Precision_Farming.tasks.send_application_reminders"
	],
	"weekly": [
		"Precision_Farming.tasks.generate_waste_summary",
		"Precision_Farming.tasks.generate_fertilizer_report"
	],
	"monthly": [
		"Precision_Farming.tasks.generate_nutrient_balance_report"
	],
}

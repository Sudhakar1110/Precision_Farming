app_name = "precision_farming"
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

after_install = "precision_farming.install.after_install"
after_migrate = "precision_farming.install.after_migrate"

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
	{"dt": "Workspace", "filters": [["name", "=", "Biogas Management"]]},
]

# Scheduled Tasks
# ---------------

scheduler_events = {
	"daily": [
		"precision_farming.tasks.check_compliance_expiry",
		"precision_farming.tasks.send_application_reminders"
	],
	"weekly": [
		"precision_farming.tasks.generate_waste_summary",
		"precision_farming.tasks.generate_fertilizer_report"
	],
	"monthly": [
		"precision_farming.tasks.generate_nutrient_balance_report"
	],
}

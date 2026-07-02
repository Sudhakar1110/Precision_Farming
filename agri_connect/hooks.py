app_name = "agri_connect"
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

after_install = "agri_connect.install.after_install"
after_migrate = "agri_connect.install.after_migrate"

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
]

# Scheduled Tasks
# ---------------

scheduler_events = {
	"daily": [
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

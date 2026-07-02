import frappe
from frappe.utils import today, add_days, nowdate

def check_compliance_expiry():
	"""Daily task to check and update expired compliance records."""
	try:
		expired_records = frappe.get_all("Compliance Record",
			filters={
				"valid_until": ("<", today()),
				"status": ("!=", "Expired")
			},
			pluck="name"
		)
		for record in expired_records:
			frappe.db.set_value("Compliance Record", record, "status", "Expired")
		if expired_records:
			frappe.db.commit()
	except Exception as e:
		frappe.log_error(f"Error in check_compliance_expiry: {str(e)}")

def send_application_reminders():
	"""Send reminders for pending fertilizer applications."""
	try:
		reminders = frappe.get_all("Fertilizer Recommendation",
			filters={
				"status": "Approved",
				"modified": ("<", add_days(nowdate(), -7))
			},
			fields=["name", "land_unit", "recommendation_date"]
		)
		for r in reminders:
			frappe.get_doc({
				"doctype": "ToDo",
				"description": f"Fertilizer Recommendation {r.name} for Land Unit {r.land_unit} is pending application.",
				"reference_type": "Fertilizer Recommendation",
				"reference_name": r.name,
				"date": today()
			}).insert(ignore_permissions=True)
	except Exception as e:
		frappe.log_error(f"Error in send_application_reminders: {str(e)}")

def generate_waste_summary():
	"""Weekly task to generate waste management summary."""
	try:
		last_week = add_days(today(), -7)
		records = frappe.get_all("Waste Record",
			filters={
				"docstatus": 1,
				"collection_date": (">=", last_week)
			},
			fields=["name", "total_organic_weight", "total_inorganic_weight", "total_weight"]
		)

		total_organic = sum(r.total_organic_weight or 0 for r in records)
		total_inorganic = sum(r.total_inorganic_weight or 0 for r in records)
		total = sum(r.total_weight or 0 for r in records)

		if total > 0:
			frappe.get_doc({
				"doctype": "Notification Log",
				"subject": f"Weekly Waste Summary: {total} kg collected",
				"email_content": f"Organic: {total_organic} kg | Inorganic: {total_inorganic} kg",
				"type": "Alert"
			}).insert(ignore_permissions=True)
	except Exception as e:
		frappe.log_error(f"Error in generate_waste_summary: {str(e)}")

def generate_fertilizer_report():
	"""Weekly task to generate fertilizer usage report."""
	try:
		last_week = add_days(today(), -7)
		applications = frappe.get_all("Fertilizer Application",
			filters={
				"docstatus": 1,
				"application_date": (">=", last_week)
			},
			fields=["name", "land_unit", "total_quantity_kg"]
		)

		total_applied = sum(a.total_quantity_kg or 0 for a in applications)
		num_applications = len(applications)

		if num_applications > 0:
			frappe.get_doc({
				"doctype": "Notification Log",
				"subject": f"Weekly Fertilizer Report: {total_applied} kg applied",
				"email_content": f"Number of applications: {num_applications}",
				"type": "Alert"
			}).insert(ignore_permissions=True)
	except Exception as e:
		frappe.log_error(f"Error in generate_fertilizer_report: {str(e)}")

def generate_nutrient_balance_report():
	"""Monthly task to generate nutrient balance report."""
	try:
		analyses = frappe.get_all("Nutrient Analysis",
			filters={
				"docstatus": 0,
				"analysis_date": (">=", add_days(today(), -30))
			},
			fields=["name", "land_unit", "n_gap_kg", "p_gap_kg", "k_gap_kg"]
		)

		total_n = sum(a.n_gap_kg or 0 for a in analyses)
		total_p = sum(a.p_gap_kg or 0 for a in analyses)
		total_k = sum(a.k_gap_kg or 0 for a in analyses)

		if analyses:
			frappe.get_doc({
				"doctype": "Notification Log",
				"subject": f"Monthly Nutrient Balance Report",
				"email_content": (
					f"Total NPK Gap required across {len(analyses)} analyses:\n"
					f"N: {total_n} kg | P: {total_p} kg | K: {total_k} kg"
				),
				"type": "Alert"
			}).insert(ignore_permissions=True)
	except Exception as e:
		frappe.log_error(f"Error in generate_nutrient_balance_report: {str(e)}")

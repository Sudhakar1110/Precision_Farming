import frappe
from frappe.model.document import Document
from frappe.utils import nowdate

class FertilizerApplication(Document):
	def validate(self):
		self.calculate_totals()

	def calculate_totals(self):
		total_qty = 0
		for item in self.get("applied_products", []):
			if item.product and item.quantity_kg:
				product = frappe.get_cached_value("Fertilizer Product", item.product,
					["nitrogen_n_percentage", "phosphorus_p_percentage", "potassium_k_percentage"],
					as_dict=True)
				if product:
					item.nitrogen_kg = item.quantity_kg * (product.nitrogen_n_percentage / 100)
					item.phosphorus_kg = item.quantity_kg * (product.phosphorus_p_percentage / 100)
					item.potassium_kg = item.quantity_kg * (product.potassium_k_percentage / 100)
				total_qty += item.quantity_kg

		self.total_quantity_kg = total_qty

	def on_submit(self):
		self.status = "Applied"
		self.create_daily_log_entry()
		self.update_recommendation_status()

	def on_cancel(self):
		self.status = "Cancelled"

	def create_daily_log_entry(self):
		if self.create_daily_log and self.land_unit:
			try:
				daily_log = frappe.new_doc("Agriculture Daily Log")
				daily_log.land_unit = self.land_unit
				daily_log.date = self.application_date or nowdate()
				daily_log.fertilizer_applied = 1
				daily_log.notes = f"Fertilizer application: {self.total_quantity_kg} kg total"
				daily_log.insert(ignore_permissions=True)
				self.daily_log = daily_log.name
			except Exception as e:
				frappe.log_error(f"Failed to create daily log for Fertilizer Application {self.name}: {str(e)}")

	def update_recommendation_status(self):
		if self.fertilizer_recommendation:
			frappe.db.set_value("Fertilizer Recommendation", self.fertilizer_recommendation, "status", "Applied")

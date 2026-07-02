import frappe
from frappe.model.document import Document
from frappe.utils import nowdate

class CompostApplication(Document):
	def validate(self):
		self.validate_compost_batch()

	def validate_compost_batch(self):
		batch = frappe.get_doc("Composting Batch", self.composting_batch)
		if batch.status != "Approved":
			frappe.throw(
				f"Composting Batch {self.composting_batch} must be approved before application."
			)
		if self.quantity_kg > (batch.output_quantity_kg or batch.output_quantity_kg or 0):
			frappe.throw(
				f"Application quantity ({self.quantity_kg} kg) exceeds batch output ({batch.output_quantity_kg or 0} kg)."
			)

	def on_submit(self):
		self.status = "Applied"
		self.create_daily_log_entry()

	def on_cancel(self):
		self.status = "Cancelled"

	def create_daily_log_entry(self):
		if self.create_daily_log and self.land_unit:
			try:
				daily_log = frappe.new_doc("Agriculture Daily Log")
				daily_log.land_unit = self.land_unit
				daily_log.crop_cycle = self.crop_cycle
				daily_log.date = self.application_date or nowdate()
				daily_log.notes = f"Compost application from batch {self.composting_batch}: {self.quantity_kg} kg applied"
				daily_log.insert(ignore_permissions=True)
				self.daily_log = daily_log.name
			except Exception as e:
				frappe.log_error(f"Failed to create daily log for Compost Application {self.name}: {str(e)}")

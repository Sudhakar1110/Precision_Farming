import frappe
from frappe.model.document import Document

class CompostApplication(Document):
	def validate(self):
		self.validate_compost_batch()

	def validate_compost_batch(self):
		batch = frappe.get_doc("Composting Batch", self.composting_batch)
		if batch.status != "Approved":
			frappe.throw(
				f"Composting Batch {self.composting_batch} must be approved before application."
			)
		if self.quantity_kg > (batch.output_quantity_kg or 0):
			frappe.throw(
				f"Application quantity ({self.quantity_kg} kg) exceeds batch output ({batch.output_quantity_kg or 0} kg)."
			)

	def on_submit(self):
		self.status = "Applied"

	def on_cancel(self):
		self.status = "Cancelled"

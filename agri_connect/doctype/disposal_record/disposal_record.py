import frappe
from frappe.model.document import Document

class DisposalRecord(Document):
	def validate(self):
		if not self.status:
			self.status = "Pending"

	def on_submit(self):
		if self.waste_record:
			frappe.db.set_value("Waste Record", self.waste_record, "classification_status", "Completed")

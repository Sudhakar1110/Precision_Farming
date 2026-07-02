import frappe
from frappe.model.document import Document

class FertilizerSchedule(Document):
	def validate(self):
		if not self.status:
			self.status = "Planned"

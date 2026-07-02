import frappe
from frappe.model.document import Document

class CollectionSchedule(Document):
	def validate(self):
		if not self.status:
			self.status = "Pending"

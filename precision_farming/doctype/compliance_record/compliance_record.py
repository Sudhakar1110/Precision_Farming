import frappe
from frappe.model.document import Document
from frappe.utils import today

class ComplianceRecord(Document):
	def validate(self):
		self.check_expiry()

	def check_expiry(self):
		if self.valid_until and self.valid_until < today():
			self.status = "Expired"

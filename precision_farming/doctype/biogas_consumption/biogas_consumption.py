import frappe
from frappe.model.document import Document
from frappe.utils import flt


class BiogasConsumption(Document):
	def validate(self):
		self.validate_quantity()

	def validate_quantity(self):
		if flt(self.quantity_m3) <= 0:
			frappe.throw("Consumption quantity must be greater than zero.")

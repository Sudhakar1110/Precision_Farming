import frappe
from frappe.model.document import Document
from frappe.utils import flt


class BiogasStorageEntry(Document):
	def validate(self):
		self.validate_quantity()
		self.fetch_warehouse_from_batch()

	def validate_quantity(self):
		if flt(self.quantity_m3) <= 0:
			frappe.throw("Quantity must be greater than zero.")

	def fetch_warehouse_from_batch(self):
		"""Auto-populate warehouse from Biogas Production Settings if not set."""
		if not self.warehouse:
			settings = frappe.get_single("Biogas Production Settings")
			if settings.default_biogas_warehouse:
				self.warehouse = settings.default_biogas_warehouse

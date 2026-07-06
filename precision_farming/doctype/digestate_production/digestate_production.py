import frappe
from frappe.model.document import Document
from frappe.utils import flt


class DigestateProduction(Document):
	def validate(self):
		self.validate_quantity()

	def validate_quantity(self):
		if flt(self.quantity_kg) <= 0:
			frappe.throw("Quantity must be greater than zero.")

	def on_submit(self):
		self.create_stock_entry()

	def on_cancel(self):
		self.cancel_stock_entry()

	def create_stock_entry(self):
		"""Create a Stock Entry for digestate if not already linked."""
		if self.digestate_stock_entry:
			return

		company = frappe.defaults.get_user_default("Company")
		if not company:
			frappe.throw("No default company set.")

		if not self.warehouse:
			settings = frappe.get_single("Biogas Production Settings")
			self.warehouse = settings.default_digestate_warehouse

		if not self.warehouse:
			frappe.throw("Please set a Warehouse for digestate storage.")

		se = frappe.new_doc("Stock Entry")
		se.stock_entry_type = "Material Receipt"
		se.company = company
		se.append("items", {
			"item_code": "Digestate",
			"t_warehouse": self.warehouse,
			"qty": self.quantity_kg,
			"uom": "Kg",
			"stock_uom": "Kg",
			"conversion_factor": 1,
			"basic_rate": 0,
		})
		se.flags.ignore_permissions = True
		se.insert()
		se.submit()

		self.db_set("digestate_stock_entry", se.name)

	def cancel_stock_entry(self):
		if self.digestate_stock_entry:
			try:
				se = frappe.get_doc("Stock Entry", self.digestate_stock_entry)
				se.cancel()
			except Exception:
				pass

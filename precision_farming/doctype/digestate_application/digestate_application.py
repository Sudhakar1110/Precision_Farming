import frappe
from frappe.model.document import Document
from frappe.utils import flt

class DigestateApplication(Document):
	def validate(self):
		self.validate_digestate_batch()
		self.calculate_application_rate()
		self.validate_available_stock()

	def validate_digestate_batch(self):
		"""Ensure the source batch/production is Completed."""
		if self.biogas_production:
			production = frappe.get_doc("Biogas Production", self.biogas_production)
			if production.status != "Completed":
				frappe.throw(
					f"Biogas Production {self.biogas_production} must be Completed before application."
				)
		elif self.biogas_production_batch:
			batch = frappe.get_doc("Biogas Production Batch", self.biogas_production_batch)
			if batch.status != "Completed":
				frappe.throw(
					f"Biogas Production Batch {self.biogas_production_batch} must be Completed before application."
				)

	def calculate_application_rate(self):
		"""Compute application rate as kg per hectare."""
		if self.area_covered and self.area_covered > 0:
			self.application_rate = flt(self.quantity_applied) / flt(self.area_covered)
		else:
			self.application_rate = 0

	def validate_available_stock(self):
		"""Check that enough Digestate stock is available."""
		warehouses = frappe.get_all("Warehouse",
			filters={"warehouse_name": ["like", "Digestate Storage%"]},
			limit=1)
		if not warehouses:
			frappe.throw("Digestate Storage warehouse not found. Please set it up first.")

		available_qty = frappe.db.get_value("Bin",
			{"item_code": "Digestate", "warehouse": warehouses[0].name},
			"actual_qty") or 0

		if flt(self.quantity_applied) > flt(available_qty):
			frappe.throw(
				f"Application quantity ({self.quantity_applied} kg) exceeds available Digestate stock "
				f"({available_qty} kg) in {warehouses[0].name}."
			)

	def on_submit(self):
		"""Create a Material Issue Stock Entry for Digestate."""
		self.status = "Applied"
		self._create_issue_stock_entry()

	def _create_issue_stock_entry(self):
		"""Create a Material Issue Stock Entry for the digestate application."""
		warehouses = frappe.get_all("Warehouse",
			filters={"warehouse_name": ["like", "Digestate Storage%"]},
			limit=1)
		if not warehouses:
			frappe.throw("Digestate Storage warehouse not found.")

		se = frappe.new_doc("Stock Entry")
		se.stock_entry_type = "Material Issue"
		se.company = frappe.defaults.get_user_default("Company")

		se.append("items", {
			"item_code": "Digestate",
			"s_warehouse": warehouses[0].name,
			"qty": self.quantity_applied,
			"uom": "Kg",
			"stock_uom": "Kg",
			"conversion_factor": 1,
			"basic_rate": 0
		})

		se.flags.ignore_permissions = True
		se.insert()
		se.submit()
		self.db_set("stock_entry", se.name)

	def on_cancel(self):
		"""Cancel the stock entry on cancel."""
		self.status = "Cancelled"
		if self.stock_entry:
			try:
				se = frappe.get_doc("Stock Entry", self.stock_entry)
				se.cancel()
			except Exception:
				pass

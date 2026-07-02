import frappe
from frappe.model.document import Document

class CompostingBatch(Document):
	def validate(self):
		self.calculate_total_input()

	def calculate_total_input(self):
		total = 0
		for ingredient in self.get("ingredients", []):
			total += ingredient.quantity_kg
		self.total_input_kg = total

	def on_submit(self):
		if self.waste_record:
			frappe.db.set_value("Waste Record", self.waste_record, "classification_status", "Processing")

	def on_cancel(self):
		if self.waste_record:
			frappe.db.set_value("Waste Record", self.waste_record, "classification_status", "Classified")

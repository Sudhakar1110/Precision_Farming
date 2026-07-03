import frappe
from frappe.model.document import Document

class MeasurementVerification(Document):
	def validate(self):
		self.calculate_deviation()

	def calculate_deviation(self):
		if self.actual_quantity_kg and self.expected_quantity_kg > 0:
			self.deviation_percentage = abs(
				(self.actual_quantity_kg - self.expected_quantity_kg) / self.expected_quantity_kg * 100
			)
			if self.deviation_percentage > 10:
				self.status = "Needs Adjustment"
			else:
				self.status = "Verified"

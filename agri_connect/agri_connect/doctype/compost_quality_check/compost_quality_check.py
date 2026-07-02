import frappe
from frappe.model.document import Document

class CompostQualityCheck(Document):
	def validate(self):
		self.evaluate_results()

	def evaluate_results(self):
		all_pass = True
		any_fail = False

		for result in self.get("results", []):
			if result.parameter:
				param = frappe.get_cached_value("Compost Quality Parameter", result.parameter,
					["acceptable_min", "acceptable_max", "unit"], as_dict=True)
				if param:
					result.acceptable_min = param.acceptable_min
					result.acceptable_max = param.acceptable_max
					result.unit = param.unit

					if param.acceptable_min is not None and param.acceptable_max is not None:
						if param.acceptable_min <= result.measured_value <= param.acceptable_max:
							result.status = "Pass"
						else:
							result.status = "Fail"
							any_fail = True
							all_pass = False
					else:
						result.status = "Pass"

		if all_pass and len(self.get("results", [])) > 0:
			self.overall_result = "Pass"
		elif any_fail:
			self.overall_result = "Fail"
		else:
			self.overall_result = "Conditional Pass"

	def on_submit(self):
		if self.overall_result == "Pass" and self.composting_batch:
			frappe.db.set_value("Composting Batch", self.composting_batch, {
				"quality_check": 1,
				"compost_quality_check": self.name,
				"status": "Approved"
			})

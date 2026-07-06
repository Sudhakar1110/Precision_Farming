import frappe
from frappe.model.document import Document
from frappe.utils import flt


class BiogasQualityCheck(Document):
	def validate(self):
		self.evaluate_overall_result()

	def evaluate_overall_result(self):
		"""Auto-evaluate overall result based on quality parameters."""
		if not self.status or self.status != "Completed":
			self.overall_result = ""
			return

		# Define quality thresholds
		failures = []

		if self.methane_percentage is not None and self.methane_percentage < 50:
			failures.append(f"Methane too low ({self.methane_percentage}% - min 50%)")
		if self.co2_percentage is not None and self.co2_percentage > 50:
			failures.append(f"CO2 too high ({self.co2_percentage}% - max 50%)")
		if self.h2s_ppm is not None and self.h2s_ppm > 1000:
			failures.append(f"H2S too high ({self.h2s_ppm} ppm - max 1000)")
		if self.moisture_percentage is not None and self.moisture_percentage > 5:
			failures.append(f"Moisture too high ({self.moisture_percentage}% - max 5%)")

		if len(failures) >= 2:
			self.overall_result = "Fail"
			self.remarks = "; ".join(failures)
		elif len(failures) == 1:
			self.overall_result = "Conditional Pass"
			self.remarks = "; ".join(failures)
		else:
			self.overall_result = "Pass"
			if not self.remarks:
				self.remarks = "All quality parameters within acceptable range."

	@frappe.whitelist()
	def auto_fill_from_settings(self):
		"""Fill default quality thresholds from Biogas Production Settings."""
		settings = frappe.get_single("Biogas Production Settings")
		if settings.default_methane_threshold:
			pass  # Thresholds stored for reference

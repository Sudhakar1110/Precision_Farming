import frappe
from frappe.model.document import Document

class SoilAnalysis(Document):
	def validate(self):
		self.calculate_nutrient_status()

	def calculate_nutrient_status(self):
		for result in self.get("results", []):
			if result.nutrient:
				threshold = frappe.get_cached_value("Soil Nutrient Threshold", result.nutrient,
					["low_threshold", "medium_threshold", "high_threshold", "unit"], as_dict=True)
				if threshold:
					result.unit = threshold.unit
					if result.value <= threshold.low_threshold:
						result.status = "Low"
					elif result.value <= threshold.medium_threshold:
						result.status = "Medium"
					else:
						result.status = "High"

		self.derive_npk_status()

	def derive_npk_status(self):
		nutrient_map = {}
		for result in self.get("results", []):
			if result.nutrient:
				nutrient_map[result.nutrient.lower()] = result.status

		self.nitrogen_status = nutrient_map.get("nitrogen (n)") or nutrient_map.get("n", "")
		self.phosphorus_status = nutrient_map.get("phosphorus (p)") or nutrient_map.get("p", "")
		self.potassium_status = nutrient_map.get("potassium (k)") or nutrient_map.get("k", "")

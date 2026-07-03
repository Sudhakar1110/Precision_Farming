import frappe
from frappe.model.document import Document

class NutrientAnalysis(Document):
	def validate(self):
		self.calculate_requirements()
		self.calculate_soil_contributions()
		self.calculate_gaps()

	def calculate_requirements(self):
		if self.crop_nutrient_standard and self.area_hectare:
			standard = frappe.get_cached_value("Crop Nutrient Standard", self.crop_nutrient_standard,
				["nitrogen_n", "phosphorus_p", "potassium_k"], as_dict=True)
			if standard:
				self.total_n_required = standard.nitrogen_n * self.area_hectare
				self.total_p_required = standard.phosphorus_p * self.area_hectare
				self.total_k_required = standard.potassium_k * self.area_hectare

	def calculate_soil_contributions(self):
		if self.soil_analysis:
			analysis = frappe.get_doc("Soil Analysis", self.soil_analysis)
			nutrient_values = {}

			for result in analysis.get("results", []):
				if result.nutrient:
					nutrient_name = result.nutrient.lower()
					if "nitrogen" in nutrient_name or nutrient_name == "n":
						nutrient_values["n"] = result.value
					elif "phosphorus" in nutrient_name or nutrient_name == "p":
						nutrient_values["p"] = result.value
					elif "potassium" in nutrient_name or nutrient_name == "k":
						nutrient_values["k"] = result.value

			self.soil_n_available = nutrient_values.get("n", 0) * self.area_hectare
			self.soil_p_available = nutrient_values.get("p", 0) * self.area_hectare
			self.soil_k_available = nutrient_values.get("k", 0) * self.area_hectare

	def calculate_gaps(self):
		compost_data = self.get_compost_contributions()

		self.compost_n_contribution = compost_data.get("n", 0)
		self.compost_p_contribution = compost_data.get("p", 0)
		self.compost_k_contribution = compost_data.get("k", 0)

		n_gap = max(0, self.total_n_required - self.soil_n_available - self.compost_n_contribution)
		p_gap = max(0, self.total_p_required - self.soil_p_available - self.compost_p_contribution)
		k_gap = max(0, self.total_k_required - self.soil_k_available - self.compost_k_contribution)

		self.n_gap_kg = n_gap
		self.p_gap_kg = p_gap
		self.k_gap_kg = k_gap

		self.update_nutrient_gap_table()

	def get_compost_contributions(self):
		"""Fetch compost application history for this land unit and calculate NPK contribution."""
		from frappe.utils import today
		data = {"n": 0, "p": 0, "k": 0}

		applications = frappe.get_all("Compost Application",
			filters={
				"land_unit": self.land_unit,
				"docstatus": 1,
				"application_date": (">=", frappe.utils.add_days(today(), -180))
			},
			fields=["quantity_kg"]
		)

		for app in applications:
			# Assume average compost NPK: 1.5% N, 0.5% P, 1.0% K
			data["n"] += app.quantity_kg * 0.015
			data["p"] += app.quantity_kg * 0.005
			data["k"] += app.quantity_kg * 0.010

		return data

	def update_nutrient_gap_table(self):
		self.set("nutrient_gap", [])
		nutrients = [
			{"nutrient": "Nitrogen (N)", "req": self.total_n_required,
			 "soil": self.soil_n_available, "compost": self.compost_n_contribution, "gap": self.n_gap_kg},
			{"nutrient": "Phosphorus (P)", "req": self.total_p_required,
			 "soil": self.soil_p_available, "compost": self.compost_p_contribution, "gap": self.p_gap_kg},
			{"nutrient": "Potassium (K)", "req": self.total_k_required,
			 "soil": self.soil_k_available, "compost": self.compost_k_contribution, "gap": self.k_gap_kg},
		]

		for n in nutrients:
			self.append("nutrient_gap", {
				"nutrient": n["nutrient"],
				"crop_requirement": n["req"],
				"soil_available": n["soil"],
				"compost_contribution": n["compost"],
				"gap": n["gap"]
			})

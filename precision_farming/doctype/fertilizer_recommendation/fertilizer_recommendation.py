import frappe
from frappe.model.document import Document

class FertilizerRecommendation(Document):
	def validate(self):
		self.populate_from_analysis()
		self.auto_calculate_products()

	def populate_from_analysis(self):
		if self.nutrient_analysis:
			analysis = frappe.get_cached_value("Nutrient Analysis", self.nutrient_analysis,
				["land_unit", "area_hectare", "n_gap_kg", "p_gap_kg", "k_gap_kg", "crop"], as_dict=True)
			if analysis:
				self.land_unit = analysis.land_unit
				self.area_hectare = analysis.area_hectare
				self.crop = analysis.crop

	def auto_calculate_products(self):
		"""Auto-calculate fertilizer product quantities based on nutrient gaps."""
		self.total_n_fertilizer = 0
		self.total_p_fertilizer = 0
		self.total_k_fertilizer = 0
		total_cost = 0

		products = self.get("recommended_products", [])
		for item in products:
			if item.product and item.product_quantity_kg:
				product = frappe.get_cached_value("Fertilizer Product", item.product,
					["nitrogen_n_percentage", "phosphorus_p_percentage", "potassium_k_percentage"],
					as_dict=True)
				if product:
					n_applied = item.product_quantity_kg * (product.nitrogen_n_percentage / 100)
					p_applied = item.product_quantity_kg * (product.phosphorus_p_percentage / 100)
					k_applied = item.product_quantity_kg * (product.potassium_k_percentage / 100)

					self.total_n_fertilizer += n_applied
					self.total_p_fertilizer += p_applied
					self.total_k_fertilizer += k_applied

	def on_submit(self):
		self.status = "Approved"
		self.approved_by = frappe.session.user
		self.db_set("status", "Approved")
		self.db_set("approved_by", frappe.session.user)

	def on_update_after_submit(self):
		if self.status == "Approved" and not self.approved_by:
			self.approved_by = frappe.session.user

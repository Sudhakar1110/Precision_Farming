import frappe
from frappe.model.document import Document
from frappe.utils import flt, today


class BiogasConversionRatio(Document):
	def validate(self):
		self.validate_dates()
		self.validate_ratio()

	def validate_dates(self):
		if self.effective_from and self.effective_to and self.effective_from > self.effective_to:
			frappe.throw("Effective From date must be before Effective To date.")

	def validate_ratio(self):
		if flt(self.conversion_ratio_m3_per_kg) <= 0:
			frappe.throw("Conversion ratio must be greater than zero.")


@frappe.whitelist()
def get_conversion_ratio(waste_type, biogas_plant=None, check_date=None):
	"""Get the applicable conversion ratio for a waste type.

	First tries to find a waste-type-specific ratio, then falls back
	to the Biogas Plant's default ratio.
	"""
	if not check_date:
		check_date = today()

	# Try to find a matching conversion ratio record
	filters = {
		"waste_type": waste_type,
		"is_active": 1,
	}
	if biogas_plant:
		filters["biogas_plant"] = ["in", [biogas_plant, "", None]]

	# or_filters must be a list of lists (Frappe API requirement)
	or_filters_list = [
		["effective_from", "<=", check_date],
		["effective_from", "is", "not set"],
	]

	ratios = frappe.get_all(
		"Biogas Conversion Ratio",
		filters=filters,
		or_filters=or_filters_list,
		fields=["conversion_ratio_m3_per_kg", "digestate_factor"],
		order_by="effective_from desc",
		limit=1
	)

	if ratios:
		return {
			"conversion_ratio": flt(ratios[0].conversion_ratio_m3_per_kg),
			"digestate_factor": flt(ratios[0].digestate_factor) or 1.5,
			"source": "Biogas Conversion Ratio"
		}

	return None

import frappe
from frappe import _


def execute(filters=None):
	"""Biogas Yield Report: shows completed batches with yield calculations."""
	if not filters:
		filters = {}

	columns = get_columns()
	data = get_data(filters)

	return columns, data


def get_columns():
	"""Return report columns."""
	return [
		{
			"fieldname": "batch_id",
			"label": _("Batch ID"),
			"fieldtype": "Link",
			"options": "Biogas Production Batch",
			"width": 150
		},
		{
			"fieldname": "biogas_plant",
			"label": _("Biogas Plant"),
			"fieldtype": "Link",
			"options": "Biogas Plant",
			"width": 150
		},
		{
			"fieldname": "land_unit",
			"label": _("Land Unit"),
			"fieldtype": "Link",
			"options": "Land Unit",
			"width": 120
		},
		{
			"fieldname": "start_date",
			"label": _("Start Date"),
			"fieldtype": "Date",
			"width": 100
		},
		{
			"fieldname": "end_date",
			"label": _("End Date"),
			"fieldtype": "Date",
			"width": 100
		},
		{
			"fieldname": "total_input_quantity",
			"label": _("Total Input (kg)"),
			"fieldtype": "Float",
			"precision": 2,
			"width": 120
		},
		{
			"fieldname": "expected_biogas_quantity",
			"label": _("Expected Biogas (m\u00b3)"),
			"fieldtype": "Float",
			"precision": 2,
			"width": 140
		},
		{
			"fieldname": "output_biogas_volume",
			"label": _("Biogas Produced (m\u00b3)"),
			"fieldtype": "Float",
			"precision": 2,
			"width": 150
		},
		{
			"fieldname": "expected_digestate_quantity",
			"label": _("Expected Digestate (kg)"),
			"fieldtype": "Float",
			"precision": 2,
			"width": 150
		},
		{
			"fieldname": "output_digestate_quantity",
			"label": _("Digestate Produced (kg)"),
			"fieldtype": "Float",
			"precision": 2,
			"width": 160
		},
		{
			"fieldname": "yield_m3_per_kg",
			"label": _("Yield (m\u00b3/kg)"),
			"fieldtype": "Float",
			"precision": 4,
			"width": 120
		},
	]


def get_data(filters):
	"""Fetch report data."""
	conditions = "bp.docstatus = 1 AND bp.status = 'Completed'"

	if filters.get("from_date"):
		conditions += f" AND bp.start_date >= '{filters['from_date']}'"
	if filters.get("to_date"):
		conditions += f" AND bp.start_date <= '{filters['to_date']}'"
	if filters.get("biogas_plant"):
		conditions += f" AND bp.biogas_plant = '{filters['biogas_plant']}'"
	if filters.get("land_unit"):
		conditions += f" AND bp.land_unit = '{filters['land_unit']}'"

	data = frappe.db.sql(f"""
		SELECT
			bp.name AS batch_id,
			bp.biogas_plant AS biogas_plant,
			bp.land_unit AS land_unit,
			bp.start_date AS start_date,
			bp.end_date AS end_date,
			bp.total_input_quantity AS total_input_quantity,
			bp.expected_biogas_quantity AS expected_biogas_quantity,
			bp.expected_digestate_quantity AS expected_digestate_quantity,
			bp.output_biogas_volume AS output_biogas_volume,
			CASE WHEN bp.total_input_quantity > 0
				THEN ROUND(bp.output_biogas_volume / bp.total_input_quantity, 4)
				ELSE 0
			END AS yield_m3_per_kg,
			bp.output_digestate_quantity AS output_digestate_quantity
		FROM `tabBiogas Production Batch` bp
		WHERE {conditions}
		ORDER BY bp.start_date DESC
	""", as_dict=1)

	return data

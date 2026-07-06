frappe.query_reports["Biogas Yield Report"] = {
	"filters": [
		{
			"fieldname": "from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			"default": frappe.datetime.month_start(),
			"reqd": 1
		},
		{
			"fieldname": "to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			"default": frappe.datetime.get_today(),
			"reqd": 1
		},
		{
			"fieldname": "biogas_plant",
			"label": __("Biogas Plant"),
			"fieldtype": "Link",
			"options": "Biogas Plant"
		},
		{
			"fieldname": "land_unit",
			"label": __("Land Unit"),
			"fieldtype": "Link",
			"options": "Land Unit"
		}
	]
};

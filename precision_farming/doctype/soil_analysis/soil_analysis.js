frappe.ui.form.on('Soil Analysis', {
	refresh: function(frm) {
		if (frm.doc.docstatus === 1) {
			frm.add_custom_button(__('Create Nutrient Analysis'), function() {
				frappe.new_doc('Nutrient Analysis', {
					land_unit: frm.doc.land_unit,
					soil_analysis: frm.doc.name,
					analysis_date: frappe.datetime.get_today()
				});
			});
		}
	}
});

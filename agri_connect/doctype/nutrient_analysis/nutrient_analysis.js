frappe.ui.form.on('Nutrient Analysis', {
	refresh: function(frm) {
		if (frm.doc.docstatus === 0 && frm.doc.n_gap_kg > 0) {
			frm.add_custom_button(__('Create Fertilizer Recommendation'), function() {
				frappe.new_doc('Fertilizer Recommendation', {
					land_unit: frm.doc.land_unit,
					crop: frm.doc.crop,
					nutrient_analysis: frm.doc.name,
					area_hectare: frm.doc.area_hectare,
					recommendation_date: frappe.datetime.get_today()
				});
			});
		}
	},

	land_unit: function(frm) {
		if (frm.doc.land_unit) {
			frappe.db.get_value('Land Unit', frm.doc.land_unit, 'area', (r) => {
				if (r && r.area) {
					frm.set_value('area_hectare', r.area);
				}
			});
		}
	}
});

frappe.ui.form.on('Biogas Consumption', {
	refresh: function(frm) {
		if (frm.doc.biogas_production) {
			frappe.db.get_value('Biogas Production', frm.doc.biogas_production,
				['output_biogas_volume', 'biogas_batch', 'land_unit'], (r) => {
					if (r) {
						if (!frm.doc.quantity_m3) {
							frm.set_value('quantity_m3', r.output_biogas_volume);
						}
						if (r.biogas_batch && !frm.doc.biogas_batch) {
							frm.set_value('biogas_batch', r.biogas_batch);
						}
						if (r.land_unit && !frm.doc.land_unit) {
							frm.set_value('land_unit', r.land_unit);
						}
					}
				});
		}
	}
});

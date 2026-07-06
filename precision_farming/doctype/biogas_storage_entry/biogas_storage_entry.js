frappe.ui.form.on('Biogas Storage Entry', {
	refresh: function(frm) {
		if (frm.doc.docstatus === 0 && frm.doc.biogas_production_batch) {
			// Auto-fetch quantity from production batch output
			frappe.db.get_value('Biogas Production Batch', frm.doc.biogas_production_batch,
				'output_biogas_volume', (r) => {
					if (r && r.output_biogas_volume && !frm.doc.quantity_m3) {
						frm.set_value('quantity_m3', r.output_biogas_volume);
					}
				});
		}
	},

	biogas_production_batch: function(frm) {
		if (frm.doc.biogas_production_batch) {
			frappe.db.get_value('Biogas Production Batch', frm.doc.biogas_production_batch,
				['output_biogas_volume', 'biogas_batch'], (r) => {
					if (r) {
						frm.set_value('quantity_m3', r.output_biogas_volume);
						if (r.biogas_batch) {
							frm.set_value('biogas_batch', r.biogas_batch);
						}
					}
				});
		}
	}
});

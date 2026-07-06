frappe.ui.form.on('Biogas Quality Check', {
	refresh: function(frm) {
		if (frm.doc.docstatus === 0) {
			// Auto-fetch biogas batch from either source
			if (frm.doc.biogas_production) {
				frappe.db.get_value('Biogas Production', frm.doc.biogas_production,
					'biogas_batch', (r) => {
						if (r && r.biogas_batch && !frm.doc.biogas_batch) {
							frm.set_value('biogas_batch', r.biogas_batch);
						}
					});
			} else if (frm.doc.biogas_production_batch) {
				frappe.db.get_value('Biogas Production Batch', frm.doc.biogas_production_batch,
					'biogas_batch', (r) => {
						if (r && r.biogas_batch && !frm.doc.biogas_batch) {
							frm.set_value('biogas_batch', r.biogas_batch);
						}
					});
			}
		}
	},

	biogas_production: function(frm) {
		if (frm.doc.biogas_production) {
			frappe.db.get_value('Biogas Production', frm.doc.biogas_production,
				'biogas_batch', (r) => {
					if (r && r.biogas_batch) {
						frm.set_value('biogas_batch', r.biogas_batch);
					}
				});
		}
	},

	biogas_production_batch: function(frm) {
		if (frm.doc.biogas_production_batch) {
			frappe.db.get_value('Biogas Production Batch', frm.doc.biogas_production_batch,
				'biogas_batch', (r) => {
					if (r && r.biogas_batch) {
						frm.set_value('biogas_batch', r.biogas_batch);
					}
				});
		}
	}
});

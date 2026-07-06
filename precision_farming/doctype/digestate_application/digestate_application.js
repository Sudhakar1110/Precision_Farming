frappe.ui.form.on('Digestate Application', {
	refresh: function(frm) {
		if (frm.doc.docstatus === 0) {
			if (frm.doc.biogas_production) {
				frappe.db.get_value('Biogas Production', frm.doc.biogas_production,
					['land_unit', 'output_digestate_quantity'], (r) => {
					if (r) {
						if (r.land_unit && !frm.doc.land_unit) {
							frm.set_value('land_unit', r.land_unit);
						}
					}
				});
			} else if (frm.doc.biogas_production_batch) {
				frappe.db.get_value('Biogas Production Batch', frm.doc.biogas_production_batch,
					['land_unit', 'output_digestate_quantity'], (r) => {
					if (r) {
						if (r.land_unit && !frm.doc.land_unit) {
							frm.set_value('land_unit', r.land_unit);
						}
					}
				});
			}
		}
	},

	biogas_production: function(frm) {
		if (frm.doc.biogas_production) {
			frappe.db.get_value('Biogas Production', frm.doc.biogas_production,
				['land_unit', 'output_digestate_quantity'], (r) => {
					if (r) {
						frm.set_value('land_unit', r.land_unit);
						if (r.output_digestate_quantity && !frm.doc.quantity_applied) {
							frm.set_value('quantity_applied', r.output_digestate_quantity);
						}
					}
				});
		}
	},

	biogas_production_batch: function(frm) {
		if (frm.doc.biogas_production_batch) {
			frappe.db.get_value('Biogas Production Batch', frm.doc.biogas_production_batch,
				['land_unit', 'output_digestate_quantity'], (r) => {
					if (r) {
						frm.set_value('land_unit', r.land_unit);
						if (r.output_digestate_quantity && !frm.doc.quantity_applied) {
							frm.set_value('quantity_applied', r.output_digestate_quantity);
						}
					}
				});
		}
	},

	area_covered: function(frm) {
		if (frm.doc.quantity_applied && frm.doc.area_covered) {
			let rate = frm.doc.quantity_applied / frm.doc.area_covered;
			frm.set_value('application_rate', rate);
		}
	},

	quantity_applied: function(frm) {
		if (frm.doc.quantity_applied && frm.doc.area_covered) {
			let rate = frm.doc.quantity_applied / frm.doc.area_covered;
			frm.set_value('application_rate', rate);
		}
	}
});

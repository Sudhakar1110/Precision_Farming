frappe.ui.form.on('Digestate Production', {
	refresh: function(frm) {
		if (frm.doc.biogas_production) {
			frappe.db.get_value('Biogas Production', frm.doc.biogas_production,
				['output_digestate_quantity', 'biogas_batch'], (r) => {
					if (r) {
						if (!frm.doc.quantity_kg) {
							frm.set_value('quantity_kg', r.output_digestate_quantity);
						}
						if (r.biogas_batch && !frm.doc.biogas_batch) {
							frm.set_value('biogas_batch', r.biogas_batch);
						}
					}
				});
		}
		if (frm.doc.docstatus === 0 && !frm.doc.warehouse) {
			frappe.call({
				method: 'frappe.client.get_single',
				args: { doctype: 'Biogas Production Settings' },
				callback: function(r) {
					if (r.message && r.message.default_digestate_warehouse) {
						frm.set_value('warehouse', r.message.default_digestate_warehouse);
					}
				}
			});
		}
	}
});

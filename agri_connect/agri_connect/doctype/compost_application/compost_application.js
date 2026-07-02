frappe.ui.form.on('Compost Application', {
	refresh: function(frm) {
		if (frm.doc.docstatus === 0 && frm.doc.composting_batch) {
			frappe.db.get_value('Composting Batch', frm.doc.composting_batch, 'output_quantity_kg', (r) => {
				if (r && r.output_quantity_kg) {
					frm.set_value('quantity_kg', r.output_quantity_kg);
				}
			});
		}
	},

	composting_batch: function(frm) {
		if (frm.doc.composting_batch) {
			frappe.db.get_value('Composting Batch', frm.doc.composting_batch,
				['land_unit', 'output_quantity_kg'], (r) => {
				if (r) {
					frm.set_value('land_unit', r.land_unit);
					if (r.output_quantity_kg) {
						frm.set_value('quantity_kg', r.output_quantity_kg);
					}
				}
			});
		}
	}
});

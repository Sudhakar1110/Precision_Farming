frappe.ui.form.on('Biogas Conversion Ratio', {
	waste_type: function(frm) {
		if (frm.doc.waste_type) {
			frappe.db.get_value('Waste Type', frm.doc.waste_type, 'waste_category', (r) => {
				if (r && r.waste_category) {
					frm.set_value('waste_category', r.waste_category);
				}
			});
		}
	}
});

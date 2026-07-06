frappe.ui.form.on('Waste Record', {
	refresh: function(frm) {
		if (frm.doc.docstatus === 1) {
			if (frm.doc.waste_category_type === 'Organic' || frm.doc.waste_category_type === 'Mixed') {
				if (!frm.doc.composting_batch) {
					frm.add_custom_button(__('Create Composting Batch'), function() {
						frappe.call({
							method: 'precision_farming.doctype.waste_record.waste_record.create_composting_batch_from_waste',
							args: {
								waste_record_name: frm.doc.name
							},
							callback: function(r) {
								if (r.message && r.message.batch) {
									frappe.set_route('Form', 'Composting Batch', r.message.batch);
								}
							}
						});
					});
				}
				if (!frm.doc.biogas_production) {
					frm.add_custom_button(__('Start Biogas Production'), function() {
						frappe.call({
							method: 'precision_farming.doctype.waste_record.waste_record.create_biogas_production_from_waste',
							args: {
								waste_record_name: frm.doc.name
							},
							callback: function(r) {
								if (r.message && r.message.production) {
									frappe.set_route('Form', 'Biogas Production', r.message.production);
								}
							}
						});
					});
				}
			}
			if (frm.doc.waste_category_type === 'Inorganic' && !frm.doc.recycling_record && !frm.doc.disposal_record) {
				frm.add_custom_button(__('Create Recycling Record'), function() {
					frappe.new_doc('Recycling Record', {
						waste_record: frm.doc.name
					});
				});
				frm.add_custom_button(__('Create Disposal Record'), function() {
					frappe.new_doc('Disposal Record', {
						waste_record: frm.doc.name
					});
				});
			}
		}
	},

	waste_items_add: function(frm, cdt, cdn) {
		let row = frappe.get_doc(cdt, cdn);
		if (row.waste_type) {
			frappe.db.get_value('Waste Type', row.waste_type, 'waste_category', (r) => {
				if (r && r.waste_category) {
					frappe.model.set_value(cdt, cdn, 'waste_category', r.waste_category);
				}
			});
		}
	}
});

frappe.ui.form.on('Waste Record Item', {
	waste_type: function(frm, cdt, cdn) {
		let row = frappe.get_doc(cdt, cdn);
		if (row.waste_type) {
			frappe.db.get_value('Waste Type', row.waste_type, 'waste_category', (r) => {
				if (r && r.waste_category) {
					frappe.model.set_value(cdt, cdn, 'waste_category', r.waste_category);
				}
			});
		}
	}
});

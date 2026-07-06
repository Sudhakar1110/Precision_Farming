frappe.ui.form.on('Waste Record', {
	refresh: function(frm) {
		if (frm.doc.docstatus === 1) {
			if ((frm.doc.waste_category_type === 'Organic' || frm.doc.waste_category_type === 'Mixed') && !frm.doc.composting_batch) {
				frm.add_custom_button(__('Create Composting Batch'), function() {
					frappe.new_doc('Composting Batch', {
						waste_record: frm.doc.name,
						land_unit: frm.doc.land_unit,
						batch_name: 'Batch from ' + frm.doc.name,
						start_date: frappe.datetime.get_today(),
						status: 'Active'
					});
				});
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

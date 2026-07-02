frappe.ui.form.on('Recycling Record', {
	refresh: function(frm) {
		if (frm.doc.docstatus === 0) {
			frm.add_custom_button(__('Fetch Waste Records'), function() {
				frappe.db.get_list('Waste Record', {
					filters: { 'waste_category_type': 'Inorganic', 'docstatus': 1, 'classification_status': 'Classified' },
					fields: ['name', 'land_unit', 'collection_date']
				}).then(records => {
					if (records.length === 0) {
						frappe.msgprint(__('No unprocessed inorganic waste records found.'));
					} else {
						let d = new frappe.ui.Dialog({
							title: __('Select Waste Record'),
							fields: [
								{ fieldtype: 'Select', fieldname: 'waste_record', label: __('Waste Record'),
									options: records.map(r => r.name) }
							],
							primary_action: function() {
								frm.set_value('waste_record', d.get_value('waste_record'));
								d.hide();
							}
						});
						d.show();
					}
				});
			});
		}
	}
});

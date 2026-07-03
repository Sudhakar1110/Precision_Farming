frappe.ui.form.on('Composting Batch', {
	refresh: function(frm) {
		if (frm.doc.docstatus === 0) {
			frm.add_custom_button(__('Add Turning Event'), function() {
				frm.add_child('turning_events', {
					turning_date: frappe.datetime.get_today()
				});
				frm.refresh_field('turning_events');
			});
		}
		if (frm.doc.docstatus === 1 && frm.doc.status === 'Ready') {
			frm.add_custom_button(__('Create Quality Check'), function() {
				frappe.new_doc('Compost Quality Check', {
					composting_batch: frm.doc.name,
					check_date: frappe.datetime.get_today()
				});
			});
		}
	},

	status: function(frm) {
		if (frm.doc.status === 'Ready') {
			frm.add_custom_button(__('Create Quality Check'), function() {
				frappe.new_doc('Compost Quality Check', {
					composting_batch: frm.doc.name
				});
			});
		}
	}
});

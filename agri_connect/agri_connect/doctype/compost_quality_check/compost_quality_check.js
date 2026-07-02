frappe.ui.form.on('Compost Quality Check', {
	refresh: function(frm) {
		if (frm.doc.docstatus === 1 && frm.doc.overall_result === 'Pass') {
			frm.add_custom_button(__('Create Compost Application'), function() {
				frappe.new_doc('Compost Application', {
					composting_batch: frm.doc.composting_batch,
					application_date: frappe.datetime.get_today()
				});
			});
		}
	}
});

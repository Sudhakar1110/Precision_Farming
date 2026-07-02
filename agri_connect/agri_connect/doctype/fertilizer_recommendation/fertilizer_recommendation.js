frappe.ui.form.on('Fertilizer Recommendation', {
	refresh: function(frm) {
		if (frm.doc.docstatus === 1 && frm.doc.status === 'Approved') {
			frm.add_custom_button(__('Create Fertilizer Application'), function() {
				frappe.new_doc('Fertilizer Application', {
					fertilizer_recommendation: frm.doc.name,
					land_unit: frm.doc.land_unit,
					crop: frm.doc.crop,
					application_date: frappe.datetime.get_today()
				});
			});
		}
	}
});

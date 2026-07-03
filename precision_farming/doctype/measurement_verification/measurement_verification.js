frappe.ui.form.on('Measurement Verification', {
	refresh: function(frm) {
		if (frm.is_new()) {
			frm.set_value('verification_date', frappe.datetime.get_today());
		}
	}
});

frappe.ui.form.on('Compliance Record', {
	refresh: function(frm) {
		// Default today's date
		if (frm.is_new()) {
			frm.set_value('compliance_date', frappe.datetime.get_today());
		}
	}
});

frappe.ui.form.on('Collection Schedule', {
	refresh: function(frm) {
		if (frm.is_new()) {
			frm.set_value('scheduled_date', frappe.datetime.get_today());
		}
	}
});

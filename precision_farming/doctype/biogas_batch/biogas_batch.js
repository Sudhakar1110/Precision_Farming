frappe.ui.form.on('Biogas Batch', {
	refresh: function(frm) {
		if (frm.doc.docstatus === 0) {
			frm.add_custom_button(__('Fetch Production Batches'), function() {
				frappe.call({
					method: 'precision_farming.doctype.biogas_batch.biogas_batch.get_batch_production_summary',
					args: { batch_name: frm.doc.name },
					callback: function(r) {
						if (r.message) {
							frm.refresh();
						}
					}
				});
			}, __('Actions'));
		}
	}
});

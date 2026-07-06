frappe.ui.form.on('Biogas Production Batch', {
	refresh: function(frm) {
		if (frm.doc.docstatus === 0 && frm.doc.status === 'Digesting') {
			frm.add_custom_button(__('Mark Completed'), function() {
				frappe.call({
					method: 'precision_farming.doctype.biogas_production_batch.biogas_production_batch.mark_completed',
					args: { batch_name: frm.doc.name },
					callback: function(r) {
						if (r.message && r.message.completed) {
							frm.refresh();
						}
					}
				});
			}, __('Actions'));
		}
		
		// Add button to create Digestate Application on completed batches
		if (frm.doc.docstatus === 1 && frm.doc.status === 'Completed') {
			frm.add_custom_button(__('Create Digestate Application'), function() {
				frappe.new_doc('Digestate Application', {
					biogas_production_batch: frm.doc.name,
					application_date: frappe.datetime.get_today(),
					land_unit: frm.doc.land_unit
				});
			});
		}
	},
	
	biogas_plant: function(frm) {
		if (frm.doc.biogas_plant) {
			frappe.db.get_value('Biogas Plant', frm.doc.biogas_plant, 'land_unit', (r) => {
				if (r && r.land_unit) {
					frm.set_value('land_unit', r.land_unit);
				}
			});
		}
	},
	
	waste_record: function(frm) {
		if (frm.doc.waste_record) {
			frappe.db.get_value('Waste Record', frm.doc.waste_record,
				['land_unit', 'total_organic_weight'], (r) => {
				if (r) {
					if (r.land_unit && !frm.doc.land_unit) {
						frm.set_value('land_unit', r.land_unit);
					}
				}
			});
		}
	}
});

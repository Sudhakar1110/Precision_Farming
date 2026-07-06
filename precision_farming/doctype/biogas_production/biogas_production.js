frappe.ui.form.on('Biogas Production', {
	refresh: function(frm) {
		if (frm.doc.docstatus === 0 && frm.doc.status === 'Digesting') {
			frm.add_custom_button(__('Mark Completed'), function() {
				frappe.call({
					method: 'precision_farming.doctype.biogas_production.biogas_production.mark_completed',
					args: { production_name: frm.doc.name },
					callback: function(r) {
						if (r.message && r.message.completed) {
							frm.refresh();
						}
					}
				});
			}, __('Actions'));

			// Create Quality Check button
			if (!frm.doc.quality_check) {
				frm.add_custom_button(__('Create Quality Check'), function() {
					frappe.new_doc('Biogas Quality Check', {
						biogas_production: frm.doc.name,
						biogas_batch: frm.doc.biogas_batch,
						check_date: frappe.datetime.get_today()
					});
				});
			}

			// Create Biogas Batch button
			if (!frm.doc.biogas_batch) {
				frm.add_custom_button(__('Create Biogas Batch'), function() {
					frappe.new_doc('Biogas Batch', {
						batch_name: 'Batch from ' + frm.doc.name,
						biogas_plant: frm.doc.biogas_plant,
						start_date: frm.doc.start_date
					});
				});
			}
		}

		// Buttons for completed/submitted documents
		if (frm.doc.docstatus === 1 && frm.doc.status === 'Completed') {
			frm.add_custom_button(__('Create Digestate Application'), function() {
				frappe.new_doc('Digestate Application', {
					biogas_production: frm.doc.name,
					application_date: frappe.datetime.get_today(),
					land_unit: frm.doc.land_unit
				});
			});

			if (frm.doc.quality_check) {
				frm.add_custom_button(__('View Quality Check'), function() {
					frappe.set_route('Form', 'Biogas Quality Check', frm.doc.quality_check);
				});
			}
		}
	},

	biogas_plant: function(frm) {
		if (frm.doc.biogas_plant) {
			frappe.db.get_value('Biogas Plant', frm.doc.biogas_plant,
				['land_unit', 'conversion_ratio'], (r) => {
					if (r) {
						if (r.land_unit) {
							frm.set_value('land_unit', r.land_unit);
						}
						frm.set_value('conversion_ratio', r.conversion_ratio);
						frm.trigger('calculate_expected_quantities');
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
						frm.trigger('calculate_expected_quantities');
					}
				});
		}
	},

	calculate_expected_quantities: function(frm) {
		if (frm.doc.total_input_quantity && frm.doc.conversion_ratio) {
			let expected_biogas = flt(frm.doc.total_input_quantity) * flt(frm.doc.conversion_ratio);
			frm.set_value('expected_biogas_quantity', expected_biogas);
			frm.set_value('expected_digestate_quantity', flt(expected_biogas) * 1.5);
		}
	}
});

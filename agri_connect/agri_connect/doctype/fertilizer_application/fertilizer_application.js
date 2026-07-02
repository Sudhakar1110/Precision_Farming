frappe.ui.form.on('Fertilizer Application', {
	refresh: function(frm) {
		if (frm.is_new()) {
			frm.set_value('application_date', frappe.datetime.get_today());
		}
	},

	fertilizer_recommendation: function(frm) {
		if (frm.doc.fertilizer_recommendation) {
			frappe.db.get_value('Fertilizer Recommendation', frm.doc.fertilizer_recommendation,
				['land_unit', 'crop', 'name'], (r) => {
				if (r) {
					frm.set_value('land_unit', r.land_unit);
					frm.set_value('crop', r.crop);
				}
			});

			// Fetch recommended products
			frappe.call({
				method: 'frappe.client.get_list',
				args: {
					doctype: 'Recommended Product',
					filters: { parent: frm.doc.fertilizer_recommendation },
					fields: ['product', 'product_quantity_kg', 'nutrient']
				},
				callback: function(r) {
					if (r.message) {
						frm.clear_table('applied_products');
						r.message.forEach(function(item) {
							let row = frm.add_child('applied_products');
							row.product = item.product;
							row.quantity_kg = item.product_quantity_kg;
							row.nutrient = item.nutrient;
						});
						frm.refresh_field('applied_products');
					}
				}
			});
		}
	}
});

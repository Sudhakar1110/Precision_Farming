import frappe
from frappe.model.document import Document
from frappe.utils import nowdate, flt

class BiogasProductionBatch(Document):
	def validate(self):
		self.calculate_total_input()
		self.calculate_yield()
		self.validate_waste_record_consumption()

	def calculate_total_input(self):
		"""Sum all input entry quantities."""
		total = 0
		for item in self.get("input_entries", []):
			total += flt(item.quantity_kg)
		self.total_input_quantity = total

	def calculate_yield(self):
		"""Compute biogas yield: volume per kg of input."""
		if self.total_input_quantity and self.output_biogas_volume:
			self.biogas_yield_m3_per_kg = flt(self.output_biogas_volume) / flt(self.total_input_quantity)
		else:
			self.biogas_yield_m3_per_kg = 0

	def validate_waste_record_consumption(self):
		"""Ensure total input doesn't exceed the source Waste Record's organic weight.

		Uses a single SQL query to sum already-consumed quantities from other
		batches linked to the same Waste Record.
		"""
		if not self.waste_record:
			return

		waste_record = frappe.get_doc("Waste Record", self.waste_record)

		# Single efficient query to sum consumed quantities
		exclusion_clause = f"AND name != {frappe.db.escape(self.name)}" if self.name else ""
		total_consumed = frappe.db.sql(f"""
			SELECT COALESCE(SUM(total_input_quantity), 0)
			FROM `tabBiogas Production Batch`
			WHERE docstatus = 1
			  AND waste_record = %s
			  {exclusion_clause}
		""", self.waste_record)[0][0]

		available = flt(waste_record.total_organic_weight) - flt(total_consumed)
		if self.total_input_quantity > available:
			frappe.throw(
				f"Total input quantity ({self.total_input_quantity} kg) exceeds available organic waste "
				f"({available} kg) from Waste Record {self.waste_record}. "
				f"Already consumed: {flt(total_consumed)} kg."
			)

	def on_submit(self):
		"""Only allow submit if status is Completed."""
		if self.status != "Completed":
			frappe.throw(
				"Biogas Production Batch must be marked as 'Completed' before submission. "
				"Use the 'Mark Completed' button to finalize the batch."
			)

	def on_cancel(self):
		"""Revert stock entries on cancel if they exist."""
		self._cancel_stock_entries()

	def _cancel_stock_entries(self):
		"""Cancel linked stock entries if they exist."""
		if self.biogas_stock_entry:
			try:
				se = frappe.get_doc("Stock Entry", self.biogas_stock_entry)
				se.cancel()
			except Exception:
				pass
		if self.digestate_stock_entry:
			try:
				se = frappe.get_doc("Stock Entry", self.digestate_stock_entry)
				se.cancel()
			except Exception:
				pass


@frappe.whitelist()
def mark_completed(batch_name):
	"""Mark a Biogas Production Batch as Completed and create Stock Entries."""
	batch = frappe.get_doc("Biogas Production Batch", batch_name)

	if batch.status == "Completed":
		frappe.msgprint(f"Batch {batch_name} is already Completed.")
		return {"batch": batch_name, "completed": True}

	if not batch.output_biogas_volume or batch.output_biogas_volume <= 0:
		frappe.throw("Biogas Produced volume must be greater than 0 before completing.")
	if not batch.output_digestate_quantity or batch.output_digestate_quantity <= 0:
		frappe.throw("Digestate Produced quantity must be greater than 0 before completing.")

	# Run validation explicitly before completing
	batch.validate()

	batch.status = "Completed"
	batch.end_date = nowdate()

	try:
		# Create Biogas Stock Entry (Material Receipt)
		if not batch.biogas_stock_entry:
			biogas_se = _create_stock_entry("Biogas", batch.output_biogas_volume, "m3", "Biogas Storage")
			batch.biogas_stock_entry = biogas_se.name

		# Create Digestate Stock Entry (Material Receipt)
		if not batch.digestate_stock_entry:
			digestate_se = _create_stock_entry("Digestate", batch.output_digestate_quantity, "Kg", "Digestate Storage")
			batch.digestate_stock_entry = digestate_se.name

		batch.flags.ignore_permissions = True
		batch.save()
		frappe.db.commit()

		# Update Waste Record classification status
		if batch.waste_record:
			frappe.db.set_value("Waste Record", batch.waste_record, "classification_status", "Completed")

		frappe.msgprint(f"Batch {batch_name} marked as Completed. Stock Entries created.")
		return {"batch": batch_name, "completed": True}

	except Exception as e:
		frappe.db.rollback()
		frappe.throw(f"Failed to complete batch: {str(e)}")


def _create_stock_entry(item_code, qty, uom, warehouse_prefix):
	"""Create a Material Receipt Stock Entry for the given item/quantity.
	
	Note: Warehouse names use the company abbreviation suffix. We look up
	by warehouse_name pattern matching since the app may be on any site.
	"""
	from frappe.utils import cstr
	
	# Find the warehouse dynamically
	warehouse_name = f"{warehouse_prefix}"
	warehouses = frappe.get_all("Warehouse", 
		filters={"warehouse_name": ["like", f"{warehouse_prefix}%"]},
		limit=1)
	
	if not warehouses:
		frappe.throw(f"Warehouse '{warehouse_prefix}' not found. Please create it via Setup.")
	
	se = frappe.new_doc("Stock Entry")
	se.stock_entry_type = "Material Receipt"
	se.company = frappe.defaults.get_user_default("Company")
	
	se.append("items", {
		"item_code": item_code,
		"t_warehouse": warehouses[0].name,
		"qty": qty,
		"uom": uom,
		"stock_uom": uom,
		"conversion_factor": 1,
		"basic_rate": 0
	})
	
	se.flags.ignore_permissions = True
	se.insert()
	se.submit()
	return se

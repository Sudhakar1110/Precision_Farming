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
		"""Ensure total input doesn't exceed the source Waste Record's organic weight."""
		if not self.waste_record:
			return

		waste_record = frappe.get_doc("Waste Record", self.waste_record)

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


def _ensure_item_exists(item_code, item_name, uom, item_group, gst_hsn_code=None):
	"""Create an Item at runtime if it doesn't exist. Returns the item code."""
	if not frappe.db.exists("Item", item_code):
		# Ensure linked records exist first
		_ensure_uom_exists(uom)
		_ensure_item_group_exists(item_group)
		if gst_hsn_code:
			_ensure_gst_hsn_code_exists(gst_hsn_code)

		item_doc = {
			"doctype": "Item",
			"item_code": item_code,
			"item_name": item_name,
			"item_group": item_group,
			"stock_uom": uom,
			"is_stock_item": 1,
		}
		if gst_hsn_code:
			item_doc["gst_hsn_code"] = gst_hsn_code

		item = frappe.get_doc(item_doc)
		item.flags.ignore_permissions = True
		item.insert()
	return item_code


def _ensure_uom_exists(uom_name):
	"""Create a UOM at runtime if it doesn't exist."""
	if not frappe.db.exists("UOM", uom_name):
		uom = frappe.get_doc({
			"doctype": "UOM",
			"uom_name": uom_name,
			"enabled": 1,
		})
		uom.flags.ignore_permissions = True
		uom.insert()


def _ensure_item_group_exists(item_group_name, parent_item_group="Products"):
	"""Create an Item Group at runtime if it doesn't exist."""
	if not frappe.db.exists("Item Group", item_group_name):
		ig = frappe.get_doc({
			"doctype": "Item Group",
			"item_group_name": item_group_name,
			"parent_item_group": parent_item_group,
			"is_group": 0,
		})
		ig.flags.ignore_permissions = True
		ig.insert()


def _ensure_gst_hsn_code_exists(hsn_code, description=None):
	"""Create a GST HSN Code at runtime if it doesn't exist."""
	if frappe.db.exists("GST HSN Code", hsn_code):
		return
	if not frappe.db.exists("DocType", "GST HSN Code"):
		return
	hsn = frappe.get_doc({
		"doctype": "GST HSN Code",
		"hsn_code": hsn_code,
		"description": description or hsn_code,
	})
	hsn.flags.ignore_permissions = True
	hsn.insert()


def _ensure_warehouse_exists(warehouse_name):
	"""Create a Warehouse at runtime if it doesn't exist. Returns the full warehouse name."""
	company = frappe.defaults.get_user_default("Company")
	if not company:
		frappe.throw("No default company set. Please set a default company first.")

	abbr = frappe.db.get_value("Company", company, "abbr")
	full_name = f"{warehouse_name} - {abbr}"

	if not frappe.db.exists("Warehouse", full_name):
		warehouse = frappe.get_doc({
			"doctype": "Warehouse",
			"warehouse_name": warehouse_name,
			"company": company,
		})
		warehouse.flags.ignore_permissions = True
		warehouse.insert()

	return full_name


def _create_stock_entry(item_code, qty, uom, warehouse_prefix):
	"""Create a Material Receipt Stock Entry for the given item/quantity.

	Auto-creates the Item, UOM, Item Group, GST HSN Code, and Warehouse
	if they do not exist yet (runtime self-healing).
	"""
	# Auto-create master data at runtime if missing
	if item_code == "Biogas":
		_ensure_item_exists("Biogas", "Biogas", "m3", "Farm Energy", "27112900")
	elif item_code == "Digestate":
		_ensure_item_exists("Digestate", "Digestate", "Kg", "Organic Inputs", "31010000")
	else:
		_ensure_item_exists(item_code, item_code, uom, "Products")

	# Ensure warehouse exists
	full_warehouse_name = _ensure_warehouse_exists(warehouse_prefix)

	se = frappe.new_doc("Stock Entry")
	se.stock_entry_type = "Material Receipt"
	se.company = frappe.defaults.get_user_default("Company")

	se.append("items", {
		"item_code": item_code,
		"t_warehouse": full_warehouse_name,
		"qty": qty,
		"uom": uom,
		"stock_uom": uom,
		"conversion_factor": 1,
		"basic_rate": 0,
	})

	se.flags.ignore_permissions = True
	se.insert()
	se.submit()
	return se

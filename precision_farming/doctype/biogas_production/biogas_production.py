import frappe
from frappe.model.document import Document
from frappe.utils import nowdate, flt


class BiogasProduction(Document):
	def validate(self):
		self.calculate_total_input()
		self.calculate_expected_quantities()
		self.calculate_yield()
		self.validate_waste_record_consumption()

	def calculate_total_input(self):
		"""Sum all production items and feedstock quantities."""
		total = 0
		for item in self.get("production_items", []):
			total += flt(item.quantity_kg)
		for item in self.get("feedstock", []):
			total += flt(item.quantity_kg)
		self.total_input_quantity = total

	def calculate_yield(self):
		"""Compute biogas yield: volume per kg of input."""
		if self.total_input_quantity and self.output_biogas_volume:
			self.biogas_yield_m3_per_kg = flt(self.output_biogas_volume) / flt(self.total_input_quantity)
		else:
			self.biogas_yield_m3_per_kg = 0

	def calculate_expected_quantities(self):
		"""Auto-calculate expected biogas/digestate from total input and conversion ratio."""
		if self.total_input_quantity and self.conversion_ratio:
			if not self.expected_biogas_quantity:
				self.expected_biogas_quantity = flt(self.total_input_quantity) * flt(self.conversion_ratio)
			if not self.expected_digestate_quantity:
				self.expected_digestate_quantity = flt(self.expected_biogas_quantity) * 1.5

	def validate_waste_record_consumption(self):
		"""Ensure total input doesn't exceed the source Waste Record's organic weight."""
		if not self.waste_record:
			return

		waste_record = frappe.get_doc("Waste Record", self.waste_record)

		exclusion_clause = f"AND name != {frappe.db.escape(self.name)}" if self.name else ""
		total_consumed = frappe.db.sql(f"""
			SELECT COALESCE(SUM(total_input_quantity), 0)
			FROM `tabBiogas Production`
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
				"Biogas Production must be marked as 'Completed' before submission. "
				"Use the 'Mark Completed' button to finalize."
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
def mark_completed(production_name):
	"""Mark a Biogas Production as Completed and create Stock Entries."""
	production = frappe.get_doc("Biogas Production", production_name)

	if production.status == "Completed":
		frappe.msgprint(f"Biogas Production {production_name} is already Completed.")
		return {"production": production_name, "completed": True}

	if not production.output_biogas_volume or production.output_biogas_volume <= 0:
		frappe.throw("Biogas Produced volume must be greater than 0 before completing.")
	if not production.output_digestate_quantity or production.output_digestate_quantity <= 0:
		frappe.throw("Digestate Produced quantity must be greater than 0 before completing.")

	production.validate()

	production.status = "Completed"
	production.end_date = nowdate()

	try:
		# Create Biogas Stock Entry (Material Receipt)
		if not production.biogas_stock_entry:
			biogas_se = _create_stock_entry("Biogas", production.output_biogas_volume, "m3", "Biogas Storage")
			production.biogas_stock_entry = biogas_se.name

		# Create Digestate Stock Entry (Material Receipt)
		if not production.digestate_stock_entry:
			digestate_se = _create_stock_entry("Digestate", production.output_digestate_quantity, "Kg", "Digestate Storage")
			production.digestate_stock_entry = digestate_se.name

		production.flags.ignore_permissions = True
		production.save()
		frappe.db.commit()

		# Update Waste Record classification status
		if production.waste_record:
			frappe.db.set_value("Waste Record", production.waste_record, "classification_status", "Completed")

		frappe.msgprint(f"Biogas Production {production_name} marked as Completed. Stock Entries created.")
		return {"production": production_name, "completed": True}

	except Exception as e:
		frappe.db.rollback()
		frappe.throw(f"Failed to complete: {str(e)}")


def _ensure_item_exists(item_code, item_name, uom, item_group, gst_hsn_code=None):
	"""Create an Item at runtime if it doesn't exist."""
	if not frappe.db.exists("Item", item_code):
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
	"""Create a Warehouse at runtime if it doesn't exist."""
	company = frappe.defaults.get_user_default("Company")
	if not company:
		frappe.throw("No default company set.")

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
	"""Create a Material Receipt Stock Entry for the given item/quantity."""
	if item_code == "Biogas":
		_ensure_item_exists("Biogas", "Biogas", "m3", "Farm Energy", "27112900")
	elif item_code == "Digestate":
		_ensure_item_exists("Digestate", "Digestate", "Kg", "Organic Inputs", "31010000")
	else:
		_ensure_item_exists(item_code, item_code, uom, "Products")

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

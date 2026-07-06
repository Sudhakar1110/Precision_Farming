import frappe
from frappe.model.document import Document
from frappe.utils import nowdate

class WasteRecord(Document):
	def validate(self):
		self.calculate_totals()
		self.classify_waste()

	def calculate_totals(self):
		total_organic = 0
		total_inorganic = 0

		for item in self.get("waste_items", []):
			if item.waste_type:
				waste_type = frappe.get_cached_value("Waste Type", item.waste_type, "waste_category")
				if waste_type:
					category_type = frappe.get_cached_value("Waste Category", waste_type, "category_type")
					if category_type == "Organic":
						total_organic += item.quantity_kg
					else:
						total_inorganic += item.quantity_kg

		self.total_organic_weight = total_organic
		self.total_inorganic_weight = total_inorganic
		self.total_weight = total_organic + total_inorganic

	def classify_waste(self):
		if self.total_organic_weight > 0 and self.total_inorganic_weight > 0:
			self.waste_category_type = "Mixed"
		elif self.total_organic_weight > 0:
			self.waste_category_type = "Organic"
		elif self.total_inorganic_weight > 0:
			self.waste_category_type = "Inorganic"
		else:
			self.waste_category_type = "Mixed"

	def on_submit(self):
		self.classification_status = "Classified"
		# Auto-create a composting batch for organic/mixed waste
		if self.waste_category_type in ("Organic", "Mixed") and self.total_organic_weight > 0:
			self._create_composting_batch()

	def on_cancel(self):
		self.classification_status = "Pending"

	def _create_composting_batch(self):
		"""Create a Composting Batch from organic waste items (auto on submit)."""
		if self.composting_batch:
			return
		if self.total_organic_weight <= 0:
			return

		batch = _make_composting_batch(self.name, self.land_unit, self.get("waste_items", []))
		if batch:
			self.db_set("composting_batch", batch.name)


@frappe.whitelist()
def create_composting_batch_from_waste(waste_record_name):
	"""Create a Composting Batch with ingredients auto-populated from a Waste Record.

	Called from the 'Create Composting Batch' button on the Waste Record form.
	Returns the batch name for navigation.
	"""
	waste_record = frappe.get_doc("Waste Record", waste_record_name)

	if waste_record.composting_batch:
		frappe.msgprint(f"Composting Batch {waste_record.composting_batch} already exists.")
		return {"batch": waste_record.composting_batch, "existing": True}

	batch = _make_composting_batch(waste_record.name, waste_record.land_unit, waste_record.get("waste_items", []))
	if not batch:
		frappe.msgprint("No organic waste items found to add as ingredients.")
		return

	frappe.db.set_value("Waste Record", waste_record_name, "composting_batch", batch.name)
	frappe.msgprint(f"Composting Batch {batch.name} created with organic waste ingredients.")
	return {"batch": batch.name, "existing": False}


def _make_composting_batch(waste_record_name, land_unit, waste_items):
	"""Shared helper: create and insert a Composting Batch with organic ingredients."""
	batch = frappe.new_doc("Composting Batch")
	batch.waste_record = waste_record_name
	batch.land_unit = land_unit
	batch.batch_name = f"Batch from {waste_record_name}"
	batch.start_date = nowdate()
	batch.status = "Active"

	for item in waste_items:
		if item.waste_type:
			waste_type_doc = frappe.get_cached_value("Waste Type", item.waste_type, "waste_category")
			if waste_type_doc:
				cat_type = frappe.get_cached_value("Waste Category", waste_type_doc, "category_type")
				if cat_type == "Organic":
					batch.append("ingredients", {
						"waste_type": item.waste_type,
						"quantity_kg": item.quantity_kg,
						"notes": item.description
					})

	if not batch.get("ingredients"):
		return None

	batch.flags.ignore_permissions = True
	batch.insert()
	return batch

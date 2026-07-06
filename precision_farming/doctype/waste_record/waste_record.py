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
			self.create_composting_batch()

	def on_cancel(self):
		self.classification_status = "Pending"

	@frappe.whitelist()
	def create_composting_batch(self):
		"""Create a Composting Batch from organic waste items.

		Called automatically on submit, or manually via the 'Create Composting Batch' button.
		"""
		if self.composting_batch:
			frappe.msgprint(f"Composting Batch {self.composting_batch} already exists for this Waste Record.")
			return

		if self.total_organic_weight <= 0:
			frappe.msgprint("No organic waste items to compost.")
			return

		batch = frappe.new_doc("Composting Batch")
		batch.waste_record = self.name
		batch.land_unit = self.land_unit
		batch.batch_name = f"Batch from {self.name}"
		batch.start_date = nowdate()
		batch.status = "Active"

		for item in self.get("waste_items", []):
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

		if batch.get("ingredients"):
			batch.flags.ignore_permissions = True
			batch.insert()
			self.db_set("composting_batch", batch.name)
			frappe.msgprint(f"Composting Batch {batch.name} created successfully.")
		return batch.name

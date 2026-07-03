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
		self.create_composting_batch()

	def on_cancel(self):
		self.classification_status = "Pending"

	def create_composting_batch(self):
		if self.waste_category_type in ("Organic", "Mixed") and self.total_organic_weight > 0:
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
				batch.insert(ignore_permissions=True)
				self.composting_batch = batch.name

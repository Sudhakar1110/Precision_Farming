import frappe
from frappe.model.document import Document
from frappe.utils import flt


class BiogasBatch(Document):
	def validate(self):
		self.calculate_totals()

	def calculate_totals(self):
		"""Calculate totals from linked Biogas Production Batch records."""
		if not self.name:
			return

		batches = frappe.get_all(
			"Biogas Production Batch",
			filters={"biogas_batch": self.name, "docstatus": 1},
			fields=["total_input_quantity", "expected_biogas_quantity", "output_biogas_volume"]
		)

		self.total_input_quantity = sum(flt(b.total_input_quantity) for b in batches)
		self.total_expected_biogas = sum(flt(b.expected_biogas_quantity) for b in batches)
		self.total_produced_biogas = sum(flt(b.output_biogas_volume) for b in batches)


@frappe.whitelist()
def get_batch_production_summary(batch_name):
	"""Return a summary of all production batches in this biogas batch."""
	batch = frappe.get_doc("Biogas Batch", batch_name)
	production_batches = frappe.get_all(
		"Biogas Production Batch",
		filters={"biogas_batch": batch_name, "docstatus": 1},
		fields=["name", "status", "output_biogas_volume", "output_digestate_quantity",
				"start_date", "end_date", "biogas_plant", "waste_record"]
	)
	return {
		"batch": batch_name,
		"total_input": batch.total_input_quantity,
		"total_expected_biogas": batch.total_expected_biogas,
		"total_produced_biogas": batch.total_produced_biogas,
		"production_batches": production_batches
	}

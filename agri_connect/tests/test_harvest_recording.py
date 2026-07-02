import frappe
from frappe.tests.utils import FrappeTestCase
from agri_connect.tests.test_fixtures import (
	get_company_abbr,
	make_crop_cycle,
	make_crop_with_produce,
	make_item,
	make_warehouse,
)


def _get_target_warehouse():
	"""Get or create a target warehouse for harvest tests."""
	abbr = get_company_abbr()
	wh_name = f"Finished Goods - {abbr}"
	if frappe.db.exists("Warehouse", wh_name):
		return wh_name
	# Fallback: use make_warehouse to create one
	wh = make_warehouse("Harvest Goods")
	return wh.name


class TestHarvestRecording(FrappeTestCase):
	def test_harvest_creation(self):
		"""Basic creation test."""
		cc = make_crop_cycle("Harvest Create Cycle")
		warehouse = _get_target_warehouse()
		doc = frappe.get_doc({
			"doctype": "Harvest Recording",
			"crop_cycle": cc.name,
			"yield_quantity": 100,
			"uom": "Nos",
			"target_warehouse": warehouse,
			"create_stock_entry": 0,
		})
		doc.insert(ignore_permissions=True)
		self.assertTrue(doc.name.startswith("AG-HR-"))

	def test_submit_creates_material_receipt(self):
		"""Submit with create_stock_entry creates Material Receipt."""
		item = make_item("Harvested Wheat")
		crop = make_crop_with_produce("Wheat Crop", "Harvested Wheat")
		cc = make_crop_cycle("Harvest Receipt Cycle", crop_name=crop.name)
		warehouse = _get_target_warehouse()

		doc = frappe.get_doc({
			"doctype": "Harvest Recording",
			"crop_cycle": cc.name,
			"yield_quantity": 50,
			"uom": "Nos",
			"target_warehouse": warehouse,
			"create_stock_entry": 1,
		})
		doc.insert(ignore_permissions=True)
		doc.submit()
		doc.reload()

		self.assertTrue(doc.stock_entry)
		se = frappe.get_doc("Stock Entry", doc.stock_entry)
		self.assertEqual(se.stock_entry_type, "Material Receipt")
		self.assertEqual(se.items[0].item_code, "Harvested Wheat")
		self.assertEqual(se.items[0].qty, 50)
		self.assertEqual(se.items[0].t_warehouse, warehouse)

	def test_submit_without_stock_entry(self):
		"""Submit with create_stock_entry=0 doesn't create SE."""
		cc = make_crop_cycle("Harvest No SE Cycle")
		warehouse = _get_target_warehouse()
		doc = frappe.get_doc({
			"doctype": "Harvest Recording",
			"crop_cycle": cc.name,
			"yield_quantity": 30,
			"uom": "Nos",
			"target_warehouse": warehouse,
			"create_stock_entry": 0,
		})
		doc.insert(ignore_permissions=True)
		doc.submit()
		doc.reload()
		self.assertFalse(doc.stock_entry)

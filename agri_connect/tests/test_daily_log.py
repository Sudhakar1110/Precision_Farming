import frappe
from frappe.tests.utils import FrappeTestCase
from agri_connect.tests.test_fixtures import (
	get_company_abbr,
	get_default_company,
	make_crop_cycle,
	make_item,
	make_stock_entry_for_item,
)


class TestAgricultureDailyLog(FrappeTestCase):
	def test_submit_without_stock_issue(self):
		"""Test that submit without issue_from_stock doesn't create SE."""
		cc = make_crop_cycle("DailyLog Cycle")
		doc = frappe.get_doc({
			"doctype": "Agriculture Daily Log",
			"crop_cycle": cc.name,
			"watered": 1,
		})
		doc.insert(ignore_permissions=True)
		doc.submit()
		self.assertFalse(doc.stock_entry)

	def test_submit_with_stock_issue_requires_warehouse(self):
		"""Test that issuing stock requires warehouse."""
		cc = make_crop_cycle("DailyLog Cycle 2")
		item = make_item("Pesticide")
		doc = frappe.get_doc({
			"doctype": "Agriculture Daily Log",
			"crop_cycle": cc.name,
			"issue_from_stock": 1,
			"item": item.name,
			"qty_used": 5,
			"uom": "Nos",
		})
		doc.insert(ignore_permissions=True)
		with self.assertRaises(Exception):
			doc.submit()

	def test_submit_with_stock_creates_material_issue(self):
		"""Submit with issue_from_stock creates a Stock Entry (Material Issue)."""
		cc = make_crop_cycle("DailyLog Stock Cycle")
		item = make_item("Test Pesticide")
		# Ensure stock exists first
		abbr = get_company_abbr()
		warehouse = f"Stores - {abbr}"
		make_stock_entry_for_item("Test Pesticide", warehouse, 100)

		doc = frappe.get_doc({
			"doctype": "Agriculture Daily Log",
			"crop_cycle": cc.name,
			"issue_from_stock": 1,
			"warehouse": warehouse,
			"item": item.name,
			"qty_used": 5,
			"uom": "Nos",
		})
		doc.insert(ignore_permissions=True)
		doc.submit()
		doc.reload()

		self.assertTrue(doc.stock_entry)
		se = frappe.get_doc("Stock Entry", doc.stock_entry)
		self.assertEqual(se.stock_entry_type, "Material Issue")
		self.assertEqual(se.docstatus, 1)  # submitted
		self.assertEqual(se.items[0].item_code, "Test Pesticide")
		self.assertEqual(se.items[0].qty, 5)

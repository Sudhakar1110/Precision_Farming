import frappe
from frappe.tests.utils import FrappeTestCase
from agri_connect.tests.test_fixtures import make_land_unit, make_crop_cycle


class TestYieldMap(FrappeTestCase):
	def test_yield_map_creation(self):
		"""Test creating a Yield Map."""
		lu = make_land_unit("Yield Farm")
		cc = make_crop_cycle("Yield Cycle")
		doc = frappe.get_doc({
			"doctype": "Yield Map",
			"land_unit": lu.name,
			"crop_cycle": cc.name,
			"total_harvest_qty": 500,
		})
		doc.insert(ignore_permissions=True)
		self.assertTrue(doc.name.startswith("YM-"))
		self.assertEqual(doc.total_harvest_qty, 500)

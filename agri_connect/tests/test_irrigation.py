import frappe
from frappe.tests.utils import FrappeTestCase
from agri_connect.tests.test_fixtures import make_land_unit


class TestIrrigationSchedule(FrappeTestCase):
	def test_default_status(self):
		"""Test that default status is 'Scheduled'."""
		lu = make_land_unit("Irrigation Farm")
		doc = frappe.get_doc({
			"doctype": "Irrigation Schedule",
			"land_unit": lu.name,
			"method": "Drip",
		})
		doc.insert(ignore_permissions=True)
		self.assertEqual(doc.status, "Scheduled")

	def test_method_is_required_field(self):
		"""Test that method field is marked as required in the meta."""
		meta = frappe.get_meta("Irrigation Schedule")
		method_field = meta.get_field("method")
		self.assertTrue(method_field.reqd)

import frappe
from frappe.tests.utils import FrappeTestCase
from agri_connect.tests.test_fixtures import make_crop_cycle


class TestCropHealthMonitor(FrappeTestCase):
	def test_health_monitor_creation(self):
		"""Test creating a Crop Health Monitor record."""
		cc = make_crop_cycle("Health Test Cycle")
		doc = frappe.get_doc({
			"doctype": "Crop Health Monitor",
			"crop_cycle": cc.name,
			"status": "Healthy",
			"health_score": 85,
		})
		doc.insert(ignore_permissions=True)
		self.assertTrue(doc.name.startswith("HLT-"))
		self.assertEqual(doc.status, "Healthy")
		self.assertEqual(doc.health_score, 85)

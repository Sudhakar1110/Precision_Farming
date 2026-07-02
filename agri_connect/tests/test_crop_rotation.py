import frappe
from frappe.tests.utils import FrappeTestCase
from agri_connect.tests.test_fixtures import make_land_unit, make_crop


class TestCropRotation(FrappeTestCase):
	def test_rotation_plan_creation(self):
		"""Test creating a Crop Rotation Plan with child items."""
		lu = make_land_unit("Rotation Farm")
		crop = make_crop("Wheat")

		doc = frappe.get_doc({
			"doctype": "Crop Rotation Plan",
			"land_unit": lu.name,
			"planned_crops": [
				{"planned_crop": crop.name, "season": "Kharif", "year": 2026},
			],
		})
		doc.insert(ignore_permissions=True)
		self.assertTrue(doc.name.startswith("ROT-"))
		self.assertEqual(len(doc.planned_crops), 1)

	def test_rotation_plan_unique_land_unit(self):
		"""Test that only one rotation plan per land unit is allowed."""
		lu = make_land_unit("Unique Farm")
		frappe.get_doc({
			"doctype": "Crop Rotation Plan",
			"land_unit": lu.name,
		}).insert(ignore_permissions=True)

		with self.assertRaises(frappe.DuplicateEntryError):
			frappe.get_doc({
				"doctype": "Crop Rotation Plan",
				"land_unit": lu.name,
			}).insert(ignore_permissions=True)

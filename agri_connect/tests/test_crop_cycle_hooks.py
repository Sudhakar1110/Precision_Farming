import frappe
from frappe.tests.utils import FrappeTestCase
from frappe.utils import nowdate
from agri_connect.tests.test_fixtures import get_default_company, make_crop, make_crop_cycle


class TestCropCycleHooks(FrappeTestCase):
	def test_custom_fields_exist(self):
		"""Test that all 7 custom fields exist on Crop Cycle."""
		meta = frappe.get_meta("Crop Cycle")
		expected_fields = [
			"land_unit", "cost_centre", "season", "budget",
			"expected_yield", "yield_unit", "actual_cost",
		]
		for field in expected_fields:
			self.assertTrue(
				meta.has_field(field),
				f"Custom field '{field}' missing from Crop Cycle",
			)

	def test_custom_field_types(self):
		"""Test that custom fields have correct types."""
		meta = frappe.get_meta("Crop Cycle")
		self.assertEqual(meta.get_field("land_unit").fieldtype, "Link")
		self.assertEqual(meta.get_field("cost_centre").fieldtype, "Link")
		self.assertEqual(meta.get_field("season").fieldtype, "Select")
		self.assertEqual(meta.get_field("budget").fieldtype, "Currency")
		self.assertEqual(meta.get_field("actual_cost").fieldtype, "Currency")
		self.assertEqual(meta.get_field("actual_cost").read_only, 1)

	def test_cost_center_synced_to_project(self):
		"""Creating Crop Cycle with cost_centre syncs it to the Project."""
		# Find a cost center
		cost_center = frappe.db.get_value("Cost Center", {"company": get_default_company(), "is_group": 0}, "name")
		if not cost_center:
			self.skipTest("No Cost Center available")

		crop = make_crop("Sync Test Crop")
		cc = frappe.get_doc({
			"doctype": "Crop Cycle",
			"title": "CC Sync Test",
			"crop": crop.name,
			"start_date": nowdate(),
			"cost_centre": cost_center,
		})
		cc.insert(ignore_permissions=True)

		if cc.project:
			project = frappe.get_doc("Project", cc.project)
			self.assertEqual(project.cost_center, cost_center)

	def test_pnl_api(self):
		"""Test Get Crop Cycle PnL API returns correct structure."""
		cc = make_crop_cycle("PnL Test Cycle")
		# Execute the Server Script directly
		frappe.form_dict.crop_cycle = cc.name
		script = frappe.get_doc("Server Script", "Get Crop Cycle PnL")
		script.execute_method()
		response = frappe.response.get("message", {})
		self.assertIn("revenue", response)
		self.assertIn("cost", response)
		self.assertIn("profit", response)

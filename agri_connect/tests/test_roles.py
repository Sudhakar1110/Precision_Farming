import frappe
from frappe.tests.utils import FrappeTestCase


class TestRoles(FrappeTestCase):
	def test_agriculture_manager_exists(self):
		"""Test that Agriculture Manager role exists."""
		self.assertTrue(frappe.db.exists("Role", "Agriculture Manager"))

	def test_agriculture_user_exists(self):
		"""Test that Agriculture User role exists."""
		self.assertTrue(frappe.db.exists("Role", "Agriculture User"))

	def test_roles_have_desk_access(self):
		"""Test that both roles have desk access enabled."""
		for role_name in ["Agriculture Manager", "Agriculture User"]:
			role = frappe.get_doc("Role", role_name)
			self.assertTrue(role.desk_access, f"{role_name} should have desk access")

	def test_farm_manager_profile_exists(self):
		"""Test that Farm Manager role profile exists."""
		self.assertTrue(frappe.db.exists("Role Profile", "Farm Manager"))

	def test_field_officer_profile_exists(self):
		"""Test that Field Officer role profile exists."""
		self.assertTrue(frappe.db.exists("Role Profile", "Field Officer"))

	def test_farm_manager_profile_roles(self):
		"""Test Farm Manager profile has correct roles."""
		doc = frappe.get_doc("Role Profile", "Farm Manager")
		roles = {r.role for r in doc.roles}
		self.assertIn("Agriculture Manager", roles)
		self.assertIn("Stock Manager", roles)
		self.assertIn("Projects Manager", roles)
		self.assertIn("Accounts User", roles)

	def test_field_officer_profile_roles(self):
		"""Test Field Officer profile has correct roles."""
		doc = frappe.get_doc("Role Profile", "Field Officer")
		roles = {r.role for r in doc.roles}
		self.assertIn("Agriculture User", roles)
		self.assertIn("Stock User", roles)
		self.assertIn("Projects User", roles)

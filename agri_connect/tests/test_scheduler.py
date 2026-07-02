import frappe
from frappe.tests.utils import FrappeTestCase


class TestScheduler(FrappeTestCase):
	def test_server_script_exists(self):
		"""Test that the Daily Agricultural Alerts server script exists."""
		exists = frappe.db.exists("Server Script", "Daily Agricultural Alerts")
		self.assertTrue(exists)

	def test_server_script_is_scheduler(self):
		"""Test that the script is a Scheduler Event type."""
		script = frappe.get_doc("Server Script", "Daily Agricultural Alerts")
		self.assertEqual(script.script_type, "Scheduler Event")
		self.assertEqual(script.cron_format, "0 8 * * *")

	def test_all_server_scripts_exist(self):
		"""Verify all expected Server Scripts are in the database."""
		expected = [
			"Labour Contract Validate",
			"Make Labour Contract JE",
			"Daily Log Stock Issue",
			"Equipment Log Validate",
			"Equipment Log Fuel Issue",
			"Harvest Recording Receipt",
			"Crop Cycle Sync Cost Center",
			"Get Crop Cycle PnL",
			"Daily Agricultural Alerts",
		]
		for name in expected:
			self.assertTrue(
				frappe.db.exists("Server Script", name),
				f"Server Script '{name}' not found"
			)

	def test_all_client_scripts_exist(self):
		"""Verify all expected Client Scripts are in the database."""
		expected = [
			"Land Unit Map",
			"Labour Contract Actions",
			"Yield Map Visualization",
		]
		for name in expected:
			self.assertTrue(
				frappe.db.exists("Client Script", name),
				f"Client Script '{name}' not found"
			)

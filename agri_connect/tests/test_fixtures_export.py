# Copyright (c) 2026, Bizaxl and contributors
# For license information, please see license.txt

import json
import os

from frappe.tests.utils import FrappeTestCase


FIXTURES_DIR = os.path.join(
	os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
	"fixtures",
)


class TestFixturesExport(FrappeTestCase):
	def test_fixtures_directory_exists(self):
		"""Test that fixtures directory exists."""
		self.assertTrue(os.path.isdir(FIXTURES_DIR))

	def test_server_script_fixture(self):
		"""Test server_script.json has all 9 scripts."""
		path = os.path.join(FIXTURES_DIR, "server_script.json")
		self.assertTrue(os.path.exists(path))
		with open(path) as f:
			data = json.load(f)
		self.assertEqual(len(data), 9)
		names = {d["name"] for d in data}
		expected = {
			"Labour Contract Validate",
			"Make Labour Contract JE",
			"Daily Log Stock Issue",
			"Equipment Log Validate",
			"Equipment Log Fuel Issue",
			"Harvest Recording Receipt",
			"Crop Cycle Sync Cost Center",
			"Get Crop Cycle PnL",
			"Daily Agricultural Alerts",
		}
		self.assertEqual(names, expected)

	def test_client_script_fixture(self):
		"""Test client_script.json has all 3 scripts."""
		path = os.path.join(FIXTURES_DIR, "client_script.json")
		self.assertTrue(os.path.exists(path))
		with open(path) as f:
			data = json.load(f)
		self.assertEqual(len(data), 3)
		names = {d["name"] for d in data}
		expected = {"Land Unit Map", "Labour Contract Actions", "Yield Map Visualization"}
		self.assertEqual(names, expected)

	def test_custom_field_fixture(self):
		"""Test custom_field.json has all 7 Crop Cycle fields."""
		path = os.path.join(FIXTURES_DIR, "custom_field.json")
		self.assertTrue(os.path.exists(path))
		with open(path) as f:
			data = json.load(f)
		self.assertEqual(len(data), 7)
		fieldnames = {d["fieldname"] for d in data}
		expected = {
			"land_unit", "cost_centre", "season", "budget",
			"expected_yield", "yield_unit", "actual_cost",
		}
		self.assertEqual(fieldnames, expected)

	def test_report_fixture(self):
		"""Test report.json has both Script Reports."""
		path = os.path.join(FIXTURES_DIR, "report.json")
		self.assertTrue(os.path.exists(path))
		with open(path) as f:
			data = json.load(f)
		self.assertEqual(len(data), 2)
		names = {d["name"] for d in data}
		self.assertIn("Crop Profitability", names)
		self.assertIn("Resource Consumption Audit", names)

	def test_number_card_fixture(self):
		"""Test number_card.json has all 4 cards."""
		path = os.path.join(FIXTURES_DIR, "number_card.json")
		self.assertTrue(os.path.exists(path))
		with open(path) as f:
			data = json.load(f)
		self.assertEqual(len(data), 4)
		names = {d["name"] for d in data}
		expected = {
			"Active Crop Cycles", "Total Land Units",
			"Pending Irrigation", "Today's Weather",
		}
		self.assertEqual(names, expected)

	def test_role_fixture(self):
		"""Test role.json has both agriculture roles."""
		path = os.path.join(FIXTURES_DIR, "role.json")
		self.assertTrue(os.path.exists(path))
		with open(path) as f:
			data = json.load(f)
		self.assertEqual(len(data), 2)
		names = {d["name"] for d in data}
		self.assertEqual(names, {"Agriculture Manager", "Agriculture User"})

	def test_role_profile_fixture(self):
		"""Test role_profile.json has both profiles."""
		path = os.path.join(FIXTURES_DIR, "role_profile.json")
		self.assertTrue(os.path.exists(path))
		with open(path) as f:
			data = json.load(f)
		self.assertEqual(len(data), 2)
		names = {d["name"] for d in data}
		self.assertEqual(names, {"Farm Manager", "Field Officer"})

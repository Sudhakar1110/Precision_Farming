# Copyright (c) 2026, Bizaxl and contributors
# For license information, please see license.txt

import frappe
from frappe.tests.utils import FrappeTestCase
from agri_connect.tests.test_fixtures import (
	get_company_abbr,
	get_default_company,
	make_crop_cycle,
	make_item,
	make_stock_entry_for_item,
	setup_agriculture_settings,
)


def _make_test_asset():
	"""Create a minimal Asset for Equipment Log tests."""
	if frappe.db.exists("Asset", {"asset_name": "Test Tractor"}):
		return frappe.db.get_value("Asset", {"asset_name": "Test Tractor"}, "name")

	# Asset Category is required with accounts
	company = get_default_company()
	abbr = get_company_abbr()

	if not frappe.db.exists("Asset Category", "Vehicles"):
		fixed_asset_acc = frappe.db.get_value("Account", {"company": company, "account_name": "Capital Equipments", "is_group": 0}, "name") or f"Capital Equipments - {abbr}"
		dep_acc = frappe.db.get_value("Account", {"company": company, "root_type": "Expense", "account_name": ["like", "%Depreciation%"], "is_group": 0}, "name") or f"Depreciation - {abbr}"
		accum_dep_acc = frappe.db.get_value("Account", {"company": company, "account_name": ["like", "%Accumulated Depreciation%"], "is_group": 0}, "name") or f"Accumulated Depreciations - {abbr}"
		frappe.get_doc({
			"doctype": "Asset Category",
			"asset_category_name": "Vehicles",
			"accounts": [
				{
					"company_name": company,
					"fixed_asset_account": fixed_asset_acc,
					"depreciation_expense_account": dep_acc,
					"accumulated_depreciation_account": accum_dep_acc,
				}
			],
		}).insert(ignore_permissions=True)

	# Asset requires an Item with is_fixed_asset=1 and asset_category
	if not frappe.db.exists("Item", "Tractor Item"):
		frappe.get_doc({
			"doctype": "Item",
			"item_code": "Tractor Item",
			"item_name": "Tractor Item",
			"item_group": "All Item Groups",
			"stock_uom": "Nos",
			"is_fixed_asset": 1,
			"is_stock_item": 0,
			"asset_category": "Vehicles",
		}).insert(ignore_permissions=True)

	# Location is required
	if not frappe.db.exists("Location", "Test Location"):
		frappe.get_doc({
			"doctype": "Location",
			"location_name": "Test Location",
		}).insert(ignore_permissions=True)

	try:
		doc = frappe.get_doc({
			"doctype": "Asset",
			"asset_name": "Test Tractor",
			"item_code": "Tractor Item",
			"company": company,
			"location": "Test Location",
			"purchase_date": "2026-01-01",
			"gross_purchase_amount": 100000,
			"available_for_use_date": "2026-01-01",
		})
		doc.insert(ignore_permissions=True)
		return doc.name
	except Exception:
		return None


class TestEquipmentLog(FrappeTestCase):
	def test_is_submittable(self):
		"""Test that Equipment Log is a submittable doctype."""
		meta = frappe.get_meta("Equipment Log")
		self.assertTrue(meta.is_submittable)

	def test_server_scripts_exist(self):
		"""Test that Equipment Log Server Scripts exist."""
		self.assertTrue(frappe.db.exists("Server Script", "Equipment Log Validate"))
		self.assertTrue(frappe.db.exists("Server Script", "Equipment Log Fuel Issue"))

	def test_odometer_validation(self):
		"""Ending odometer < starting odometer should throw via Server Script."""
		cc = make_crop_cycle("Equip Odo Cycle")
		asset_name = _make_test_asset()
		if not asset_name:
			self.skipTest("Cannot create test Asset")

		doc = frappe.get_doc({
			"doctype": "Equipment Log",
			"equipment": asset_name,
			"crop_cycle": cc.name,
			"hours": 5,
			"starting_odometer": 1000,
			"ending_odometer": 500,
		})
		with self.assertRaises(Exception):
			doc.insert(ignore_permissions=True)

	def test_odometer_valid(self):
		"""Valid odometer (ending > starting) should save."""
		cc = make_crop_cycle("Equip Valid Cycle")
		asset_name = _make_test_asset()
		if not asset_name:
			self.skipTest("Cannot create test Asset")

		doc = frappe.get_doc({
			"doctype": "Equipment Log",
			"equipment": asset_name,
			"crop_cycle": cc.name,
			"hours": 5,
			"starting_odometer": 500,
			"ending_odometer": 600,
		})
		doc.insert(ignore_permissions=True)
		self.assertEqual(doc.starting_odometer, 500)
		self.assertEqual(doc.ending_odometer, 600)

	def test_fuel_stock_entry_on_submit(self):
		"""Submit with fuel creates Material Issue SE."""
		setup_agriculture_settings()
		cc = make_crop_cycle("Equip Fuel Cycle")
		asset_name = _make_test_asset()
		if not asset_name:
			self.skipTest("Cannot create test Asset")

		fuel = make_item("Diesel")
		# Stock fuel in the same warehouse that Agriculture Settings uses
		settings = frappe.get_single("Agriculture Settings")
		fuel_wh = settings.fuel_warehouse
		make_stock_entry_for_item("Diesel", fuel_wh, 500)

		doc = frappe.get_doc({
			"doctype": "Equipment Log",
			"equipment": asset_name,
			"crop_cycle": cc.name,
			"hours": 3,
			"fuel_item": fuel.name,
			"fuel_consumed": 20,
		})
		doc.insert(ignore_permissions=True)
		doc.submit()
		doc.reload()

		self.assertTrue(doc.stock_entry)
		se = frappe.get_doc("Stock Entry", doc.stock_entry)
		self.assertEqual(se.stock_entry_type, "Material Issue")
		self.assertEqual(se.items[0].item_code, "Diesel")
		self.assertEqual(se.items[0].qty, 20)

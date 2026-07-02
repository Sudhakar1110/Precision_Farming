import frappe
from frappe.utils import nowdate


def get_default_company():
	"""Get the default company for the site."""
	return frappe.db.get_default("company") or frappe.db.get_single_value("Global Defaults", "default_company")


def get_company_abbr(company=None):
	"""Get the company abbreviation."""
	if not company:
		company = get_default_company()
	return frappe.get_cached_value("Company", company, "abbr")


def make_land_unit(name="Test Farm", area=10, area_unit="Acre"):
	"""Create or return a Land Unit for testing."""
	full_name = f"LU-{name}"
	if frappe.db.exists("Land Unit", full_name):
		return frappe.get_doc("Land Unit", full_name)
	doc = frappe.get_doc({
		"doctype": "Land Unit",
		"land_unit_name": name,
		"area": area,
		"area_unit": area_unit,
	})
	doc.insert(ignore_permissions=True)
	return doc


def make_crop(name="Test Crop"):
	"""Create or return a Crop for testing."""
	if frappe.db.exists("Crop", name):
		return frappe.get_doc("Crop", name)
	doc = frappe.get_doc({
		"doctype": "Crop",
		"title": name,
		"crop_name": name,
		"agriculture_task": [
			{
				"task_name": "Sowing",
				"start_day": 1,
				"end_day": 10,
			}
		],
	})
	doc.insert(ignore_permissions=True)
	return doc


def make_crop_cycle(title="Test Cycle", crop_name=None, land_unit=None):
	"""Create a Crop Cycle for testing."""
	if not crop_name:
		crop = make_crop()
		crop_name = crop.name
	doc = frappe.get_doc({
		"doctype": "Crop Cycle",
		"title": title,
		"crop": crop_name,
		"start_date": nowdate(),
	})
	if land_unit:
		doc.land_unit = land_unit
	doc.insert(ignore_permissions=True)
	return doc


def make_item(name="Test Item", item_group="All Item Groups", valuation_rate=1):
	"""Create or return an Item for testing."""
	if frappe.db.exists("Item", name):
		return frappe.get_doc("Item", name)
	doc = frappe.get_doc({
		"doctype": "Item",
		"item_code": name,
		"item_name": name,
		"item_group": item_group,
		"stock_uom": "Nos",
		"valuation_rate": valuation_rate,
	})
	doc.insert(ignore_permissions=True)
	return doc


def make_warehouse(name="Test Warehouse"):
	"""Create or return a Warehouse for testing."""
	abbr = get_company_abbr()
	full_name = f"{name} - {abbr}"
	if frappe.db.exists("Warehouse", full_name):
		return frappe.get_doc("Warehouse", full_name)
	doc = frappe.get_doc({
		"doctype": "Warehouse",
		"warehouse_name": name,
		"company": get_default_company(),
	})
	doc.insert(ignore_permissions=True)
	return doc


def make_crop_with_produce(name, item_name):
	"""Create or return a Crop with a produce child row linking to an Item."""
	if frappe.db.exists("Crop", name):
		return frappe.get_doc("Crop", name)
	item = make_item(item_name)
	doc = frappe.get_doc({
		"doctype": "Crop",
		"title": name,
		"crop_name": name,
		"agriculture_task": [
			{
				"task_name": "Sowing",
				"start_day": 1,
				"end_day": 10,
			}
		],
		"produce": [
			{
				"item_code": item.name,
				"qty": 1,
				"uom": "Nos",
				"rate": 0,
			}
		],
	})
	doc.insert(ignore_permissions=True)
	return doc


def setup_agriculture_settings():
	"""Set up Agriculture Settings for testing."""
	abbr = get_company_abbr()
	company = get_default_company()

	# Find a valid expense account
	expense_account = frappe.db.get_value(
		"Account",
		{"company": company, "root_type": "Expense", "is_group": 0},
		"name",
	)
	# Find a valid cash/bank account
	cash_account = frappe.db.get_value(
		"Account",
		{"company": company, "account_type": ["in", ["Cash", "Bank"]], "is_group": 0},
		"name",
	)
	# Find or create a warehouse
	fuel_warehouse = frappe.db.get_value(
		"Warehouse",
		{"company": company, "is_group": 0},
		"name",
	)

	settings = frappe.get_single("Agriculture Settings")
	settings.labour_expense_account = expense_account
	settings.default_cash_account = cash_account
	settings.fuel_warehouse = fuel_warehouse
	settings.equipment_hourly_rate = 100
	settings.save(ignore_permissions=True)


def make_stock_entry_for_item(item_name, warehouse, qty):
	"""Create a Material Receipt Stock Entry to ensure stock exists."""
	item = make_item(item_name)
	doc = frappe.get_doc({
		"doctype": "Stock Entry",
		"stock_entry_type": "Material Receipt",
		"company": get_default_company(),
		"items": [
			{
				"item_code": item.name,
				"qty": qty,
				"t_warehouse": warehouse,
				"uom": "Nos",
				"basic_rate": 1,
			}
		],
	})
	doc.insert(ignore_permissions=True)
	doc.submit()
	return doc

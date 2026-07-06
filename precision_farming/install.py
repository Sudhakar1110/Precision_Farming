import frappe


def after_install():
	"""Post-install setup: create roles, activate domain, link module, create master data."""
	create_roles()
	activate_agriculture_domain()
	link_module_to_domain()
	create_biogas_master_data()


def after_migrate():
	"""Re-apply customizations on every bench migrate: ensure roles, domain, module linkage, and master data."""
	create_roles()
	activate_agriculture_domain()
	link_module_to_domain()
	create_biogas_master_data()


def create_roles():
	"""Create Agriculture Manager and Agriculture User roles for waste and fertilizer management."""
	for role_name in ["Agriculture Manager", "Agriculture User"]:
		if not frappe.db.exists("Role", role_name):
			role = frappe.get_doc({
				"doctype": "Role",
				"role_name": role_name,
				"desk_access": 1,
				"restrict_to_domain": "Agriculture",
			})
			role.insert(ignore_permissions=True)
	frappe.db.commit()


def activate_agriculture_domain():
	"""Activate the Agriculture domain if not already active."""
	if not frappe.db.exists("Domain", "Agriculture"):
		return

	ds = frappe.get_doc("Domain Settings")
	active = [d.domain for d in ds.active_domains]
	if "Agriculture" not in active:
		ds.append("active_domains", {"domain": "Agriculture"})
		ds.save(ignore_permissions=True)
		frappe.db.commit()


def link_module_to_domain():
	"""Link the Precision Farming Module Def to the Agriculture domain.

	This ensures users with Agriculture-restricted roles (Agriculture Manager,
	Agriculture User) can see all Precision Farming DocTypes in the workspace.
	"""
	if frappe.db.exists("Module Def", "Precision Farming"):
		module_def = frappe.get_doc("Module Def", "Precision Farming")
		if module_def.restrict_to_domain != "Agriculture":
			module_def.restrict_to_domain = "Agriculture"
			module_def.save(ignore_permissions=True)
			frappe.db.commit()


def create_biogas_master_data():
	"""Create UOMs, GST HSN Codes, Items and Warehouses needed for the Biogas Management module."""
	create_uom_if_not_exists("m3")
	create_uom_if_not_exists("Kg")
	# GST HSN codes must exist before Items can reference them (India Compliance)
	create_gst_hsn_code_if_not_exists("31010000", "Organic fertilizers")
	create_gst_hsn_code_if_not_exists("27112900", "Other petroleum gases")
	create_item_if_not_exists("Biogas", "Biogas", "m3", "Farm Energy", "27112900")
	create_item_if_not_exists("Digestate", "Digestate", "Kg", "Organic Inputs", "31010000")
	create_warehouse_if_not_exists("Biogas Storage")
	create_warehouse_if_not_exists("Digestate Storage")


def create_uom_if_not_exists(uom_name):
	"""Create a UOM if it doesn't already exist."""
	if not frappe.db.exists("UOM", uom_name):
		uom = frappe.get_doc({
			"doctype": "UOM",
			"uom_name": uom_name,
			"enabled": 1,
		})
		uom.insert(ignore_permissions=True)
		frappe.db.commit()


def create_gst_hsn_code_if_not_exists(hsn_code, description):
	"""Create a GST HSN Code if it doesn't already exist."""
	if frappe.db.exists("GST HSN Code", hsn_code):
		return
	# If India Compliance / GST HSN Code doctype is not installed, skip silently
	if not frappe.db.exists("DocType", "GST HSN Code"):
		return
	hsn = frappe.get_doc({
		"doctype": "GST HSN Code",
		"hsn_code": hsn_code,
		"description": description,
	})
	hsn.insert(ignore_permissions=True)
	frappe.db.commit()


def create_item_if_not_exists(item_code, item_name, uom, item_group, gst_hsn_code=None):
	"""Create an Item if it doesn't already exist."""
	if not frappe.db.exists("Item", item_code):
		item_doc = {
			"doctype": "Item",
			"item_code": item_code,
			"item_name": item_name,
			"item_group": item_group,
			"stock_uom": uom,
			"is_stock_item": 1,
		}
		if gst_hsn_code:
			item_doc["gst_hsn_code"] = gst_hsn_code

		item = frappe.get_doc(item_doc)
		item.insert(ignore_permissions=True)
		frappe.db.commit()


def create_warehouse_if_not_exists(warehouse_name):
	"""Create a Warehouse if it doesn't already exist."""
	company = frappe.defaults.get_user_default("Company")
	if not company:
		return

	abbr = frappe.db.get_value("Company", company, "abbr")
	full_name = f"{warehouse_name} - {abbr}"
	
	if not frappe.db.exists("Warehouse", full_name):
		warehouse = frappe.get_doc({
			"doctype": "Warehouse",
			"warehouse_name": warehouse_name,
			"company": company,
		})
		warehouse.insert(ignore_permissions=True)
		frappe.db.commit()

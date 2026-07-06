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
	"""Link the Precision Farming Module Def to the Agriculture domain."""
	if frappe.db.exists("Module Def", "Precision Farming"):
		module_def = frappe.get_doc("Module Def", "Precision Farming")
		if module_def.restrict_to_domain != "Agriculture":
			module_def.restrict_to_domain = "Agriculture"
			module_def.save(ignore_permissions=True)
			frappe.db.commit()


def create_biogas_master_data():
	"""Create all master data needed by the Biogas Management module.

	Order matters — every link an Item references must exist in the DB first.
	"""
	create_uom_if_not_exists("m3")
	create_uom_if_not_exists("Kg")
	create_gst_hsn_code_if_not_exists("31010000", "Organic fertilizers")
	create_gst_hsn_code_if_not_exists("27112900", "Other petroleum gases")
	# Item Groups must exist before Items reference them
	create_item_group_if_not_exists("Farm Energy", "Products")
	create_item_group_if_not_exists("Organic Inputs", "Products")
	create_item_if_not_exists("Biogas", "Biogas", "m3", "Farm Energy", "27112900")
	create_item_if_not_exists("Digestate", "Digestate", "Kg", "Organic Inputs", "31010000")
	create_warehouse_if_not_exists("Biogas Storage")
	create_warehouse_if_not_exists("Digestate Storage")
	create_biogas_production_settings_if_not_exists()
	create_biogas_management_workspace_if_not_exists()


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
	if not frappe.db.exists("DocType", "GST HSN Code"):
		return
	hsn = frappe.get_doc({
		"doctype": "GST HSN Code",
		"hsn_code": hsn_code,
		"description": description,
	})
	hsn.insert(ignore_permissions=True)
	frappe.db.commit()


def create_item_group_if_not_exists(item_group, parent_item_group):
	"""Create an Item Group if it doesn't already exist."""
	if not frappe.db.exists("Item Group", item_group):
		ig = frappe.get_doc({
			"doctype": "Item Group",
			"item_group_name": item_group,
			"parent_item_group": parent_item_group,
			"is_group": 0,
		})
		ig.insert(ignore_permissions=True)
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


def create_biogas_production_settings_if_not_exists():
	"""Create the Biogas Production Settings singleton if not already present."""
	if frappe.db.exists("Biogas Production Settings", "Biogas Production Settings"):
		return
	settings = frappe.get_doc({
		"doctype": "Biogas Production Settings",
		"setting_name": "Biogas Production Settings",
		"default_conversion_ratio": 0.50,
		"digestate_factor": 1.50,
		"default_methane_threshold": 50.0,
		"default_co2_threshold": 50.0,
		"default_h2s_threshold": 1000,
		"enable_auto_stock_entry": 1,
	})
	settings.insert(ignore_permissions=True)
	frappe.db.commit()


def create_biogas_management_module_def_if_not_exists():
	"""Create the Biogas Management Module Def if not already present.

	Frappe auto-creates Module Defs when syncing DocTypes, but ONLY when the DocType
	is first created. Since these DocTypes were created in a previous migration (when
	their module field may have been different), the Module Def may not exist. We must
	create it explicitly so the workspace and DocTypes are properly grouped.
	"""
	if frappe.db.exists("Module Def", "Biogas Management"):
		return
	module_def = frappe.get_doc({
		"doctype": "Module Def",
		"module_name": "Biogas Management",
		"app_name": "precision_farming",
	})
	module_def.insert(ignore_permissions=True)
	frappe.db.commit()


def _build_biogas_workspace_content():
	"""Build the workspace content (visual card layout) as a JSON string.

	Using json.dumps() here instead of reading from the workspace JSON file
	avoids nested-JSON escaping errors in the file's content field.
	"""
	import json
	content = [
		{
			"id": "wo1",
			"type": "workflow_overview",
			"data": {
				"col": 12,
				"workflows": [
					{
						"label": "Biogas Production",
						"doctypes": [
							{"doctype": "Biogas Production Batch", "label": "Production", "icon": "biotech", "status_type": "Active"},
							{"doctype": "Biogas Quality Check", "label": "Quality Check", "icon": "check", "status_type": "Active"},
							{"doctype": "Biogas Storage Entry", "label": "Storage", "icon": "warehouse", "status_type": "Done"},
							{"doctype": "Digestate Application", "label": "Digestate App.", "icon": "agriculture", "status_type": "Done"},
						],
					}
				],
			},
		},
		{"id": "spacer1", "type": "spacer", "data": {"col": 12}},
		{
			"id": "header1",
			"type": "header",
			"data": {
				"col": 12,
				"text": '<span class="h4"><b>Masters</b></span>',
			},
		},
		{"id": "card1", "type": "card", "data": {"card_name": "Settings", "col": 6}},
		{"id": "card2", "type": "card", "data": {"card_name": "Infrastructure", "col": 6}},
		{"id": "spacer2", "type": "spacer", "data": {"col": 12}},
		{
			"id": "header2",
			"type": "header",
			"data": {
				"col": 12,
				"text": '<span class="h4"><b>Transactions</b></span>',
			},
		},
		{"id": "card3", "type": "card", "data": {"card_name": "Production", "col": 4}},
		{"id": "card4", "type": "card", "data": {"card_name": "Quality & Storage", "col": 4}},
		{"id": "card5", "type": "card", "data": {"card_name": "Output", "col": 4}},
	]
	return json.dumps(content)


def create_biogas_management_workspace_if_not_exists():
	"""Create the Biogas Management workspace.

	Uses 'Precision Farming' module to avoid LinkValidationError during migration.
	Workspace still appears as 'Biogas Management' in the Desk.
	"""
	import json, os

	ws_path = os.path.join(os.path.dirname(__file__), 'workspace', 'biogas_management', 'biogas_management.json')
	with open(ws_path) as f:
		ws_data = json.load(f)

	# Ensure Module Def exists before workspace (Module Def is used by workspace sync)
	create_biogas_management_module_def_if_not_exists()

	# If workspace already exists (possibly from a previous partial/failed migration),
	# delete it so we can re-create it cleanly from the JSON source of truth
	if frappe.db.exists("Workspace", "Biogas Management"):
		frappe.delete_doc("Workspace", "Biogas Management", ignore_permissions=True, force=True)
		frappe.db.commit()

	# Strip metadata keys that shouldn't be passed to frappe.get_doc() on insert
	# Keep 'doctype' — frappe.get_doc() requires it
	for meta_key in ("name", "creation", "modified", "modified_by", "owner"):
		ws_data.pop(meta_key, None)

	# Ensure 'title' is set — Frappe v15 workspace validate() calls strip_html(title)
	# and crashes if title is None
	if not ws_data.get("title"):
		ws_data["title"] = ws_data.get("label", "Biogas Management")

	# Use 'Precision Farming' (existing module) to avoid LinkValidationError
	ws_data["module"] = "Precision Farming"

	# Rename is_public → public for Frappe v15 (workspace sync maps this internally
	# but frappe.get_doc() does not — the field is named 'public' in v15 Workspace DocType)
	if "is_public" in ws_data:
		ws_data["public"] = ws_data.pop("is_public")

	# Build content programmatically with json.dumps() to avoid nested-JSON escaping errors
	ws_data["content"] = _build_biogas_workspace_content()

	workspace = frappe.get_doc(ws_data)
	workspace.flags.ignore_permissions = True
	workspace.flags.ignore_links = True
	workspace.insert()
	frappe.db.commit()

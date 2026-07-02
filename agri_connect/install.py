import json

import frappe


def after_install():
	"""Post-install setup: create roles, profiles, number cards, customize home, hide workspaces, activate domain."""
	create_roles()
	create_role_profiles()
	create_number_cards()
	customize_home_workspace()
	hide_workspaces()
	activate_agriculture_domain()


def after_migrate():
	"""Re-apply workspace customizations on every bench migrate."""
	customize_home_workspace()
	hide_workspaces()


def create_roles():
	"""Create Agriculture Manager and Agriculture User roles."""
	for role_name in ["Agriculture Manager", "Agriculture User"]:
		if not frappe.db.exists("Role", role_name):
			frappe.get_doc({
				"doctype": "Role",
				"role_name": role_name,
				"desk_access": 1,
			}).insert(ignore_permissions=True)
	frappe.db.commit()


def create_role_profiles():
	"""Create Farm Manager and Field Officer role profiles."""
	profiles = {
		"Farm Manager": [
			"Agriculture Manager", "Stock Manager", "Projects Manager", "Accounts User",
		],
		"Field Officer": [
			"Agriculture User", "Stock User", "Projects User",
		],
	}
	for profile_name, roles in profiles.items():
		if not frappe.db.exists("Role Profile", profile_name):
			doc = frappe.get_doc({
				"doctype": "Role Profile",
				"role_profile": profile_name,
			})
			for role in roles:
				if frappe.db.exists("Role", role):
					doc.append("roles", {"role": role})
			doc.insert(ignore_permissions=True)
	frappe.db.commit()


def create_number_cards():
	"""Create Number Card documents needed by the Home workspace."""
	cards = [
		{
			"name": "Active Crop Cycles",
			"label": "Active Crop Cycles",
			"document_type": "Crop Cycle",
			"function": "Count",
			"filters_json": "[]",
			"color": "#2490EF",
			"show_percentage_stats": 0,
			"is_standard": 0,
			"module": "Agri Connect",
		},
		{
			"name": "Total Land Units",
			"label": "Total Land Units",
			"document_type": "Land Unit",
			"function": "Count",
			"filters_json": "[]",
			"color": "#29CD42",
			"show_percentage_stats": 0,
			"is_standard": 0,
			"module": "Agri Connect",
		},
		{
			"name": "Pending Irrigation",
			"label": "Pending Irrigation",
			"document_type": "Irrigation Schedule",
			"function": "Count",
			"filters_json": "[[\"Irrigation Schedule\",\"status\",\"=\",\"Scheduled\"]]",
			"color": "#ECAD4B",
			"show_percentage_stats": 0,
			"is_standard": 0,
			"module": "Agri Connect",
		},
		{
			"name": "Today's Weather",
			"label": "Today's Weather",
			"document_type": "Weather Log",
			"function": "Count",
			"filters_json": "[]",
			"dynamic_filters_json": "[[\"Weather Log\",\"date\",\"=\",\"frappe.datetime.get_today()\"]]",
			"color": "#7578F6",
			"show_percentage_stats": 0,
			"is_standard": 0,
			"module": "Agri Connect",
		},
	]
	for card in cards:
		if not frappe.db.exists("Number Card", card["label"]):
			frappe.get_doc({"doctype": "Number Card", **card}).insert(ignore_permissions=True)
	frappe.db.commit()


def customize_home_workspace():
	"""Inject Farm Management content into the Home workspace."""
	if not frappe.db.exists("Workspace", "Home"):
		return

	ws = frappe.get_doc("Workspace", "Home")

	# Build the new content
	content = _get_farm_home_content()
	ws.content = json.dumps(content)

	# Replace shortcuts
	ws.shortcuts = []
	for shortcut in [
		{"label": "Land Unit", "link_to": "Land Unit", "type": "DocType", "color": "#29CD42"},
		{"label": "Crop Cycle", "link_to": "Crop Cycle", "type": "DocType", "color": "#2490EF"},
		{"label": "Daily Log", "link_to": "Agriculture Daily Log", "type": "DocType", "color": "#ECAD4B"},
		{"label": "Equipment Log", "link_to": "Equipment Log", "type": "DocType", "color": "#7578F6"},
	]:
		ws.append("shortcuts", shortcut)

	# Add number cards
	ws.number_cards = []
	for nc in [
		{"number_card_name": "Active Crop Cycles", "label": "Active Crop Cycles"},
		{"number_card_name": "Total Land Units", "label": "Total Land Units"},
		{"number_card_name": "Pending Irrigation", "label": "Pending Irrigation"},
		{"number_card_name": "Today's Weather", "label": "Today's Weather"},
	]:
		ws.append("number_cards", nc)

	# Replace links/cards
	ws.links = []
	for link in _get_farm_card_links():
		ws.append("links", link)

	ws.save(ignore_permissions=True)
	frappe.db.commit()


def _get_farm_home_content():
	"""Return the content blocks for the farm-focused Home workspace."""
	return [
		{
			"id": "wo1", "type": "workflow_overview",
			"data": {
				"col": 12,
				"workflows": [
					{
						"label": "Crop Lifecycle",
						"doctypes": [
							{"doctype": "Land Unit", "label": "Land Unit", "icon": "map", "status_type": "Active"},
							{"doctype": "Crop Cycle", "label": "Crop Cycle", "icon": "branch", "status_type": "Active"},
							{"doctype": "Agriculture Daily Log", "label": "Daily Log", "icon": "file", "status_type": "Active"},
							{"doctype": "Harvest Recording", "label": "Harvest", "icon": "income", "status_type": "Done"},
							{"doctype": "Yield Map", "label": "Yield Map", "icon": "gantt", "status_type": "Done"},
						],
					},
					{
						"label": "Field Operations",
						"doctypes": [
							{"doctype": "Irrigation Schedule", "label": "Irrigation", "icon": "calendar", "status_type": "Pending"},
							{"doctype": "Equipment Log", "label": "Equipment", "icon": "tool", "status_type": "Active"},
							{"doctype": "Labour Contract", "label": "Labour", "icon": "users", "status_type": "Active"},
						],
					},
					{
						"label": "Monitoring & Analytics",
						"doctypes": [
							{"doctype": "Weather Log", "label": "Weather", "icon": "agriculture", "status_type": "Active"},
							{"doctype": "IoT Sensor Reading", "label": "IoT Sensors", "icon": "dashboard", "status_type": "Active"},
							{"doctype": "Crop Health Monitor", "label": "Crop Health", "icon": "healthcare", "status_type": "Pending"},
							{"doctype": "Crop Rotation Plan", "label": "Rotation Plan", "icon": "list", "status_type": "Done"},
						],
					},
				],
			},
		},
		{"id": "spacer0", "type": "spacer", "data": {"col": 12}},
		{"id": "nc1", "type": "number_card", "data": {"number_card_name": "Active Crop Cycles", "col": 3}},
		{"id": "nc2", "type": "number_card", "data": {"number_card_name": "Total Land Units", "col": 3}},
		{"id": "nc3", "type": "number_card", "data": {"number_card_name": "Pending Irrigation", "col": 3}},
		{"id": "nc4", "type": "number_card", "data": {"number_card_name": "Today's Weather", "col": 3}},
		{"id": "spacer1", "type": "spacer", "data": {"col": 12}},
		{"id": "header1", "type": "header", "data": {"text": "<span class=\"h4\"><b>Quick Access</b></span>", "col": 12}},
		{"id": "sc1", "type": "shortcut", "data": {"shortcut_name": "Land Unit", "col": 3}},
		{"id": "sc2", "type": "shortcut", "data": {"shortcut_name": "Crop Cycle", "col": 3}},
		{"id": "sc3", "type": "shortcut", "data": {"shortcut_name": "Daily Log", "col": 3}},
		{"id": "sc4", "type": "shortcut", "data": {"shortcut_name": "Equipment Log", "col": 3}},
		{"id": "spacer2", "type": "spacer", "data": {"col": 12}},
		{"id": "header2", "type": "header", "data": {"text": "<span class=\"h4\"><b>Reports & Settings</b></span>", "col": 12}},
		{"id": "card1", "type": "card", "data": {"card_name": "Crops & Lands", "col": 4}},
		{"id": "card2", "type": "card", "data": {"card_name": "Field Operations", "col": 4}},
		{"id": "card3", "type": "card", "data": {"card_name": "Analytics & GIS", "col": 4}},
		{"id": "card4", "type": "card", "data": {"card_name": "IoT & Monitoring", "col": 4}},
		{"id": "card5", "type": "card", "data": {"card_name": "Labour & Workers", "col": 4}},
		{"id": "card6", "type": "card", "data": {"card_name": "Setup", "col": 4}},
	]


def _get_farm_card_links():
	"""Return the card link definitions for the farm Home workspace.
	Skips Report links if the report doesn't exist yet (fixtures not loaded).
	"""
	all_links = [
		{"type": "Card Break", "label": "Crops & Lands", "link_type": "DocType", "link_count": 3},
		{"type": "Link", "label": "Crop", "link_to": "Crop", "link_type": "DocType", "onboard": 1},
		{"type": "Link", "label": "Crop Cycle", "link_to": "Crop Cycle", "link_type": "DocType", "onboard": 1},
		{"type": "Link", "label": "Land Unit", "link_to": "Land Unit", "link_type": "DocType", "onboard": 1},
		{"type": "Card Break", "label": "Field Operations", "link_type": "DocType", "link_count": 4},
		{"type": "Link", "label": "Agriculture Daily Log", "link_to": "Agriculture Daily Log", "link_type": "DocType"},
		{"type": "Link", "label": "Equipment Log", "link_to": "Equipment Log", "link_type": "DocType"},
		{"type": "Link", "label": "Irrigation Schedule", "link_to": "Irrigation Schedule", "link_type": "DocType"},
		{"type": "Link", "label": "Harvest Recording", "link_to": "Harvest Recording", "link_type": "DocType"},
		{"type": "Card Break", "label": "Labour & Workers", "link_type": "DocType", "link_count": 1},
		{"type": "Link", "label": "Labour Contract", "link_to": "Labour Contract", "link_type": "DocType"},
		{"type": "Card Break", "label": "Analytics & GIS", "link_type": "DocType", "link_count": 4},
		{"type": "Link", "label": "Weather Log", "link_to": "Weather Log", "link_type": "DocType"},
		{"type": "Link", "label": "Yield Map", "link_to": "Yield Map", "link_type": "DocType"},
		{"type": "Link", "label": "Crop Profitability", "link_to": "Crop Profitability", "link_type": "Report"},
		{"type": "Link", "label": "Resource Consumption Audit", "link_to": "Resource Consumption Audit", "link_type": "Report"},
		{"type": "Card Break", "label": "IoT & Monitoring", "link_type": "DocType", "link_count": 2},
		{"type": "Link", "label": "IoT Sensor Reading", "link_to": "IoT Sensor Reading", "link_type": "DocType"},
		{"type": "Link", "label": "Crop Health Monitor", "link_to": "Crop Health Monitor", "link_type": "DocType"},
		{"type": "Card Break", "label": "Setup", "link_type": "DocType", "link_count": 4},
		{"type": "Link", "label": "Agriculture Settings", "link_to": "Agriculture Settings", "link_type": "DocType"},
		{"type": "Link", "label": "Crop Rotation Plan", "link_to": "Crop Rotation Plan", "link_type": "DocType"},
		{"type": "Link", "label": "Disease", "link_to": "Disease", "link_type": "DocType"},
		{"type": "Link", "label": "Fertilizer", "link_to": "Fertilizer", "link_type": "DocType"},
	]
	# Filter out links whose targets don't exist yet (e.g., Reports from fixtures)
	filtered = []
	for link in all_links:
		if link["type"] == "Card Break":
			filtered.append(link)
		elif link.get("link_type") == "Report":
			if frappe.db.exists("Report", link["link_to"]):
				filtered.append(link)
		else:
			filtered.append(link)
	return filtered


def hide_workspaces():
	"""Hide ERPNext workspaces not relevant to agriculture."""
	hide_list = [
		"Financial Reports",
		"Payables",
		"Receivables",
		"Buying",
		"Selling",
		"CRM",
		"Manufacturing",
		"Quality",
		"Support",
		"Projects",
		"ERPNext Integrations",
		"Build",
		"Integrations",
		"Tools",
		"Website",
		"Users",
		"Welcome Workspace",
		"Farm Management",
	]
	for ws_name in hide_list:
		if frappe.db.exists("Workspace", ws_name):
			frappe.db.set_value("Workspace", ws_name, "is_hidden", 1)

	# Set sidebar icons for visible workspaces
	icon_map = {
		"Home": "lc-house",
		"Accounting": "lc-wallet",
		"Agriculture": "agriculture",
		"Stock": "lc-package",
		"Assets": "lc-monitor-smartphone",
	}
	for ws_name, icon in icon_map.items():
		if frappe.db.exists("Workspace", ws_name):
			frappe.db.set_value("Workspace", ws_name, "icon", icon)

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

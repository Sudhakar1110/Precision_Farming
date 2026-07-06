import frappe, json


def fix():
	"""Fix the Precision Farming workspace to show all 3 workflow sections.

	Run via: bench --site your-site execute precision_farming.fix_workspace.fix
	"""
	ws_name = "Precision Farming"
	if not frappe.db.exists("Workspace", ws_name):
		print(f"❌ Workspace '{ws_name}' not found in database")
		return

	ws = frappe.get_doc("Workspace", ws_name)

	content = json.dumps([
		{
			"id": "wo1",
			"type": "workflow_overview",
			"data": {
				"col": 12,
				"workflows": [
					{
						"label": "Waste Management",
						"doctypes": [
							{"doctype": "Waste Record", "label": "Waste Collection", "icon": "list", "status_type": "Active"},
							{"doctype": "Composting Batch", "label": "Composting", "icon": "branch", "status_type": "Active"},
							{"doctype": "Compost Application", "label": "Field Application", "icon": "agriculture", "status_type": "Done"}
						]
					},
					{
						"label": "Inorganic Waste",
						"doctypes": [
							{"doctype": "Waste Record", "label": "Waste Collection", "icon": "list", "status_type": "Active"},
							{"doctype": "Recycling Record", "label": "Recycling", "icon": "cycle", "status_type": "Active"},
							{"doctype": "Disposal Record", "label": "Disposal", "icon": "delete", "status_type": "Done"}
						]
					},
					{
						"label": "Fertilizer Management",
						"doctypes": [
							{"doctype": "Soil Analysis", "label": "Soil Test", "icon": "healthcare", "status_type": "Active"},
							{"doctype": "Nutrient Analysis", "label": "NPK Analysis", "icon": "dashboard", "status_type": "Active"},
							{"doctype": "Fertilizer Recommendation", "label": "Recommendation", "icon": "clipboard", "status_type": "Pending"},
							{"doctype": "Fertilizer Application", "label": "Application", "icon": "agriculture", "status_type": "Done"}
						]
					}
				]
			}
		},
		{"id": "spacer1", "type": "spacer", "data": {"col": 12}},
		{"id": "header2", "type": "header", "data": {"text": '<span class="h4"><b>Agriculture Waste Management</b></span>', "col": 12}},
		{"id": "card1", "type": "card", "data": {"card_name": "Waste Collection", "col": 3}},
		{"id": "card2", "type": "card", "data": {"card_name": "Composting", "col": 3}},
		{"id": "card3", "type": "card", "data": {"card_name": "Disposal & Recycling", "col": 3}},
		{"id": "card7", "type": "card", "data": {"card_name": "Compliance & Records", "col": 3}},
		{"id": "spacer2", "type": "spacer", "data": {"col": 12}},
		{"id": "header3", "type": "header", "data": {"text": '<span class="h4"><b>Fertilizer Measurement</b></span>', "col": 12}},
		{"id": "card4", "type": "card", "data": {"card_name": "Soil & Nutrient Analysis", "col": 3}},
		{"id": "card5", "type": "card", "data": {"card_name": "Fertilizer Planning", "col": 3}},
		{"id": "card6", "type": "card", "data": {"card_name": "Setup", "col": 3}},
		{"id": "card8", "type": "card", "data": {"card_name": "Measurement & Verification", "col": 3}}
	])

	ws.content = content
	ws.title = "Precision Farming"
	ws.label = "Precision Farming"
	ws.public = 1
	ws.is_hidden = 0
	ws.hide_custom = 0
	ws.roles = []
	ws.for_user = ""
	ws.save(ignore_permissions=True)
	frappe.db.commit()

	print("✅ Precision Farming workspace fixed!")
	print("")
	print("   Workflow sections now visible:")
	print("   - Waste Management (Waste Record -> Composting Batch -> Compost Application)")
	print("   - Inorganic Waste (Waste Record -> Recycling Record -> Disposal Record)")
	print("   - Fertilizer Management (Soil Analysis -> Nutrient Analysis -> Fertilizer Rec. -> Fertilizer Application)")
	print("")
	print("   8 Card sections:")
	print("   Waste Collection | Composting | Disposal & Recycling | Compliance & Records")
	print("   Soil & Nutrient Analysis | Fertilizer Planning | Setup | Measurement & Verification")


def create_land_unit():
	"""Create a demo Land Unit named 'Demo Farm' for testing.

	Run via: bench --site your-site execute precision_farming.fix_workspace.create_land_unit
	"""
	expected_name = "Demo Farm"

	if frappe.db.exists("Land Unit", expected_name):
		print(f"  Land Unit '{expected_name}' already exists")
		return

	for existing in frappe.get_all("Land Unit", filters={"land_unit_name": "Demo Farm"}):
		if existing.name != expected_name:
			old_name = existing.name
			frappe.rename_doc("Land Unit", old_name, expected_name, force=True)
			frappe.db.commit()
			print(f"  Land Unit renamed from '{old_name}' to '{expected_name}'")
			print(f"  You can now use '{expected_name}' in all Land Unit fields.")
			return

	lu = frappe.get_doc({
		"doctype": "Land Unit",
		"land_unit_name": expected_name,
		"unit_type": "Hectare",
		"area_in_hectare": 5.0
	})
	lu.flags.ignore_links = True
	lu.insert()

	if lu.name != expected_name:
		generated_name = lu.name
		frappe.rename_doc("Land Unit", generated_name, expected_name, force=True)
		frappe.db.commit()
		print(f"  Land Unit created as '{generated_name}', renamed to '{expected_name}'")
	else:
		frappe.db.commit()
		print(f"  Land Unit '{expected_name}' created successfully!")

	print(f"  You can now use '{expected_name}' in all Land Unit fields.")


def fix_all_references():
	"""Rename all auto-generated demo records so cross-references work.

	The demo data creates records with auto-generated names (FR-2026-00001)
	but uses hardcoded names (DEMO-FR-001) in link fields. This renames
	all records to DEMO-* names so links resolve properly on submit.

	Run via: bench --site your-site execute precision_farming.fix_workspace.fix_all_references
	"""
	print("=" * 60)
	print("Fixing demo record name references...")
	print("=" * 60)

	# Map of (doctype, actual_name, desired_name)
	# Uses naming_series pattern to find records
	renames = [
		("Waste Record", "WR-2026-00001", "DEMO-WR-001"),
		("Composting Batch", "CB-2026-00001", "DEMO-CB-001"),
		("Compost Application", "CA-2026-00001", "DEMO-CA-001"),
		("Soil Analysis", "SA-2026-00001", "DEMO-SA-001"),
		("Nutrient Analysis", "NA-2026-00001", "DEMO-NA-001"),
		("Fertilizer Recommendation", "FR-2026-00001", "DEMO-FR-001"),
		("Fertilizer Application", "FA-2026-00001", "DEMO-FA-001"),
		("Fertilizer Schedule", "FS-2026-00001", "DEMO-FS-001"),
		("Recycling Record", "RR-2026-00001", "DEMO-RR-001"),
		("Disposal Record", "DR-2026-00001", "DEMO-DR-001"),
		("Collection Schedule", "CS-2026-00001", "DEMO-CS-001"),
		("Compliance Record", "CR-2026-00001", "DEMO-CR-001"),
		("Measurement Verification", "MV-2026-00001", "DEMO-MV-001"),
	]

	# Also try to find records by their naming series pattern if exact name not found
	count = 0
	for doctype, actual_name, desired_name in renames:
		if frappe.db.exists(doctype, desired_name):
			print(f"  {desired_name} already exists, skipping")
			continue

		if frappe.db.exists(doctype, actual_name):
			frappe.rename_doc(doctype, actual_name, desired_name, force=True)
			frappe.db.commit()
			print(f"  Renamed: {actual_name} -> {desired_name}")
			count += 1
		else:
			# Try to find any record with matching naming series pattern
			records = frappe.get_all(doctype, filters={"name": ["like", f"{actual_name[:3]}%"]}, limit=1)
			if records:
				frappe.rename_doc(doctype, records[0].name, desired_name, force=True)
				frappe.db.commit()
				print(f"  Renamed: {records[0].name} -> {desired_name}")
				count += 1
			else:
				print(f"  No record found for {doctype} matching '{actual_name}' or pattern")

	# Also fix the Compost Quality Check which uses format naming
	cq_records = frappe.get_all("Compost Quality Check", filters={
		"composting_batch": "DEMO-CB-001"
	}, limit=1)
	if cq_records and cq_records[0].name != "DEMO-CQ-001":
		if not frappe.db.exists("Compost Quality Check", "DEMO-CQ-001"):
			frappe.rename_doc("Compost Quality Check", cq_records[0].name, "DEMO-CQ-001", force=True)
			frappe.db.commit()
			print(f"  Renamed: {cq_records[0].name} -> DEMO-CQ-001")
			count += 1

	print(f"\n  Total records renamed: {count}")
	print("  All link references should now resolve correctly!")


if __name__ == "__main__":
	fix()

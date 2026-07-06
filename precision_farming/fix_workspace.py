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
	print("   🌿 Waste Management (Waste Record → Composting Batch → Compost Application)")
	print("   ♻️ Inorganic Waste (Waste Record → Recycling Record → Disposal Record)")
	print("   🌾 Fertilizer Management (Soil Analysis → Nutrient Analysis → Fertilizer Rec. → Fertilizer Application)")
	print("")
	print("   8 Card sections:")
	print("   Waste Collection | Composting | Disposal & Recycling | Compliance & Records")
	print("   Soil & Nutrient Analysis | Fertilizer Planning | Setup | Measurement & Verification")


if __name__ == "__main__":
	fix()

import frappe
from frappe.utils import today, add_days


def create_demo_data():
	"""Create comprehensive demo data for the Precision Farming application.

	All records use DEMO-* names so cross-references work correctly on submit.

	Run via: bench --site your-site execute precision_farming.demo.create_demo_data
	"""
	print("=" * 60)
	print("Creating Precision Farming demo data...")
	print("=" * 60)

	_ensure_land_unit("Demo Farm")
	_create_waste_record()
	_create_composting_batch()
	_create_compost_quality_check()
	_create_compost_application()
	_create_soil_analysis()
	_create_nutrient_analysis()
	_create_fertilizer_recommendation()
	_create_fertilizer_application()
	_create_fertilizer_schedule()
	_create_recycling_record()
	_create_disposal_record()
	_create_collection_schedule()
	_create_compliance_record()
	_create_measurement_verification()

	frappe.db.commit()
	print("\n" + "=" * 60)
	print("All demo data created successfully!")
	print("=" * 60)


def _insert_and_rename(doc_dict, expected_name):
	"""Insert a document and rename it to the expected DEMO-* name.

	The naming series auto-generates names like 'WR-2026-00001', but cross-references
	use DEMO-* names. This helper inserts and renames to ensure link consistency.
	"""
	doc = frappe.get_doc(doc_dict)
	doc.flags.ignore_validate = True
	doc.flags.ignore_links = True
	doc.flags.ignore_permissions = True
	doc.insert()
	if doc.name != expected_name:
		frappe.rename_doc(doc_dict["doctype"], doc.name, expected_name, force=True)
		frappe.db.commit()
	print(f"  {doc_dict['doctype']}: {expected_name}")
	return doc


def _ensure_land_unit(name):
	"""Ensure a Land Unit exists (from ERPNext Agriculture module)."""
	if not frappe.db.exists("Land Unit", name):
		lu = frappe.get_doc({
			"doctype": "Land Unit",
			"land_unit_name": name,
			"unit_type": "Hectare",
			"area_in_hectare": 5.0
		})
		lu.flags.ignore_validate = True
		lu.flags.ignore_links = True
		lu.flags.ignore_permissions = True
		lu.insert()
		if lu.name != name:
			frappe.rename_doc("Land Unit", lu.name, name, force=True)
			frappe.db.commit()
		print(f"  Land Unit: {name}")


def _create_waste_record():
	if frappe.db.exists("Waste Record", "DEMO-WR-001"):
		print("  Waste Record already exists")
		return

	_insert_and_rename({
		"doctype": "Waste Record",
		"naming_series": "WR-.YYYY.-",
		"land_unit": "Demo Farm",
		"collection_date": today(),
		"location": "Field A-1, North Block",
		"waste_items": [
			{"waste_type": "Crop Residue", "waste_category": "Organic Waste", "quantity_kg": 500, "source": "Crop Residue"},
			{"waste_type": "Weeds", "waste_category": "Organic Waste", "quantity_kg": 150, "source": "Weeding"},
			{"waste_type": "Empty Fertilizer Bags", "waste_category": "Inorganic Waste", "quantity_kg": 25, "source": "Packaging"}
		]
	}, "DEMO-WR-001")


def _create_composting_batch():
	if frappe.db.exists("Composting Batch", "DEMO-CB-001"):
		print("  Composting Batch already exists")
		return

	_insert_and_rename({
		"doctype": "Composting Batch",
		"naming_series": "CB-.YYYY.-",
		"waste_record": "DEMO-WR-001",
		"land_unit": "Demo Farm",
		"batch_name": "Spring Compost Batch 2026",
		"start_date": today(),
		"status": "Active",
		"method": "Aerobic",
		"ingredients": [
			{"waste_type": "Crop Residue", "quantity_kg": 500, "carbon_ratio": 60},
			{"waste_type": "Weeds", "quantity_kg": 150, "carbon_ratio": 25}
		],
		"turning_events": [
			{"turning_date": today(), "temperature_celsius": 55, "moisture_percentage": 50, "notes": "First turning - good heat generation"}
		]
	}, "DEMO-CB-001")


def _create_compost_quality_check():
	if frappe.db.exists("Compost Quality Check", {"composting_batch": "DEMO-CB-001"}):
		print("  Compost Quality Check already exists")
		return

	_insert_and_rename({
		"doctype": "Compost Quality Check",
		"composting_batch": "DEMO-CB-001",
		"check_date": today(),
		"results": [
			{"parameter": "Temperature", "measured_value": 55.0},
			{"parameter": "Moisture Content", "measured_value": 48.0},
			{"parameter": "Carbon to Nitrogen Ratio", "measured_value": 30.0},
			{"parameter": "pH Level", "measured_value": 7.2}
		]
	}, "DEMO-CQ-001")


def _create_compost_application():
	if frappe.db.exists("Compost Application", {"composting_batch": "DEMO-CB-001"}):
		print("  Compost Application already exists")
		return

	_insert_and_rename({
		"doctype": "Compost Application",
		"naming_series": "CA-.YYYY.-",
		"composting_batch": "DEMO-CB-001",
		"land_unit": "Demo Farm",
		"application_date": add_days(today(), 60),
		"quantity_kg": 550,
		"application_method": "Broadcasting"
	}, "DEMO-CA-001")


def _create_soil_analysis():
	if frappe.db.exists("Soil Analysis", "DEMO-SA-001"):
		print("  Soil Analysis already exists")
		return

	_insert_and_rename({
		"doctype": "Soil Analysis",
		"naming_series": "SA-.YYYY.-",
		"land_unit": "Demo Farm",
		"analysis_date": today(),
		"lab_name": "AgriTest Lab",
		"results": [
			{"nutrient": "Nitrogen (N)", "value": 45.0, "unit": "kg/ha"},
			{"nutrient": "Phosphorus (P)", "value": 22.0, "unit": "kg/ha"},
			{"nutrient": "Potassium (K)", "value": 180.0, "unit": "kg/ha"},
			{"nutrient": "pH Level", "value": 6.8, "unit": "pH"},
			{"nutrient": "Organic Matter", "value": 1.2, "unit": "%"}
		]
	}, "DEMO-SA-001")


def _create_nutrient_analysis():
	if frappe.db.exists("Nutrient Analysis", "DEMO-NA-001"):
		print("  Nutrient Analysis already exists")
		return

	_insert_and_rename({
		"doctype": "Nutrient Analysis",
		"naming_series": "NA-.YYYY.-",
		"land_unit": "Demo Farm",
		"area_hectare": 2.0,
		"soil_analysis": "DEMO-SA-001",
		"crop_nutrient_standard": "Paddy (Rice)",
		"growth_stage": "Vegetative",
		"analysis_date": today(),
		"soil_n_available": 45.0,
		"soil_p_available": 22.0,
		"soil_k_available": 180.0,
		"total_n_required": 240.0,
		"total_p_required": 120.0,
		"total_k_required": 120.0,
		"nutrient_gap": [
			{"nutrient": "Nitrogen (N)", "crop_requirement": 240.0, "soil_available": 45.0, "gap": 195.0},
			{"nutrient": "Phosphorus (P)", "crop_requirement": 120.0, "soil_available": 22.0, "gap": 98.0},
			{"nutrient": "Potassium (K)", "crop_requirement": 120.0, "soil_available": 180.0, "gap": 0}
		]
	}, "DEMO-NA-001")


def _create_fertilizer_recommendation():
	if frappe.db.exists("Fertilizer Recommendation", "DEMO-FR-001"):
		print("  Fertilizer Recommendation already exists")
		return

	_insert_and_rename({
		"doctype": "Fertilizer Recommendation",
		"naming_series": "FR-.YYYY.-",
		"land_unit": "Demo Farm",
		"nutrient_analysis": "DEMO-NA-001",
		"area_hectare": 2.0,
		"recommendation_date": today(),
		"status": "Draft",
		"recommended_products": [
			{"product": "Urea (46% N)", "nutrient": "Nitrogen (N)", "gap_to_fill": 195.0, "product_quantity_kg": 424.0},
			{"product": "DAP (18-46-0)", "nutrient": "Phosphorus (P)", "gap_to_fill": 98.0, "product_quantity_kg": 213.0}
		]
	}, "DEMO-FR-001")


def _create_fertilizer_application():
	if frappe.db.exists("Fertilizer Application", "DEMO-FA-001"):
		print("  Fertilizer Application already exists")
		return

	_insert_and_rename({
		"doctype": "Fertilizer Application",
		"naming_series": "FA-.YYYY.-",
		"fertilizer_recommendation": "DEMO-FR-001",
		"land_unit": "Demo Farm",
		"application_date": today(),
		"application_method": "Broadcasting",
		"status": "Draft",
		"applied_products": [
			{"product": "Urea (46% N)", "quantity_kg": 200},
			{"product": "DAP (18-46-0)", "quantity_kg": 100}
		]
	}, "DEMO-FA-001")


def _create_fertilizer_schedule():
	if frappe.db.exists("Fertilizer Schedule", "DEMO-FS-001"):
		print("  Fertilizer Schedule already exists")
		return

	_insert_and_rename({
		"doctype": "Fertilizer Schedule",
		"naming_series": "FS-.YYYY.-",
		"land_unit": "Demo Farm",
		"start_date": today(),
		"end_date": add_days(today(), 90),
		"status": "Planned",
		"schedule_items": [
			{"planned_date": add_days(today(), 7), "product": "Urea (46% N)", "quantity_kg": 100, "application_method": "Broadcasting", "status": "Pending"},
			{"planned_date": add_days(today(), 14), "product": "DAP (18-46-0)", "quantity_kg": 75, "application_method": "Banding", "status": "Pending"},
			{"planned_date": add_days(today(), 30), "product": "MOP (0-0-60)", "quantity_kg": 50, "application_method": "Side Dressing", "status": "Pending"}
		]
	}, "DEMO-FS-001")


def _create_recycling_record():
	if frappe.db.exists("Recycling Record", "DEMO-RR-001"):
		print("  Recycling Record already exists")
		return

	_insert_and_rename({
		"doctype": "Recycling Record",
		"naming_series": "RR-.YYYY.-",
		"waste_record": "DEMO-WR-001",
		"recycling_date": today(),
		"material_type": "Plastic",
		"quantity_kg": 25,
		"recycler": "Green Earth Recyclers",
		"status": "Sent to Recycling"
	}, "DEMO-RR-001")


def _create_disposal_record():
	if frappe.db.exists("Disposal Record", "DEMO-DR-001"):
		print("  Disposal Record already exists")
		return

	_insert_and_rename({
		"doctype": "Disposal Record",
		"naming_series": "DR-.YYYY.-",
		"waste_record": "DEMO-WR-001",
		"disposal_date": today(),
		"disposal_method": "Landfill",
		"quantity_kg": 10,
		"disposal_facility": "City Sanitary Landfill",
		"status": "Compliant",
		"notes": "Non-recyclable inorganic waste disposed per regulations"
	}, "DEMO-DR-001")


def _create_collection_schedule():
	if frappe.db.exists("Collection Schedule", {"land_unit": "Demo Farm"}):
		print("  Collection Schedule already exists")
		return

	_insert_and_rename({
		"doctype": "Collection Schedule",
		"naming_series": "CS-.YYYY.-",
		"land_unit": "Demo Farm",
		"scheduled_date": add_days(today(), 3),
		"status": "Pending"
	}, "DEMO-CS-001")


def _create_compliance_record():
	if frappe.db.exists("Compliance Record", "DEMO-CR-001"):
		print("  Compliance Record already exists")
		return

	_insert_and_rename({
		"doctype": "Compliance Record",
		"naming_series": "CR-.YYYY.-",
		"waste_record": "DEMO-WR-001",
		"compliance_type": "Environmental",
		"compliance_date": today(),
		"valid_until": add_days(today(), 365),
		"status": "Compliant",
		"issuing_authority": "Agriculture Department",
		"notes": "Annual waste management compliance check passed"
	}, "DEMO-CR-001")


def _create_measurement_verification():
	if frappe.db.exists("Measurement Verification", "DEMO-MV-001"):
		print("  Measurement Verification already exists")
		return

	_insert_and_rename({
		"doctype": "Measurement Verification",
		"naming_series": "MV-.YYYY.-",
		"land_unit": "Demo Farm",
		"verification_date": today(),
		"expected_quantity_kg": 500,
		"actual_quantity_kg": 485,
		"status": "Verified"
	}, "DEMO-MV-001")


if __name__ == "__main__":
	create_demo_data()

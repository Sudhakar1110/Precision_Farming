"""Fix missing Biogas Management DocTypes.

Run via: bench --site YOUR-SITE execute precision_farming.fix_missing_doctypes.fix
"""
import frappe, json, os


def get_biogas_doctype_paths():
    """Return paths to all biogas DocType JSON files in dependency order."""
    app_path = frappe.get_app_path("precision_farming")
    base = os.path.join(app_path, "doctype")

    # Order matters: DocTypes with no Link fields first,
    # then DocTypes that reference earlier ones
    doctype_dirs = [
        "biogas_production_settings",  # Single - no dependencies
        "biogas_conversion_ratio",     # Master - no dependencies
        "biogas_production_item",      # Child Table - depends on Biogas Production
        "biogas_feedstock",            # Child Table - depends on Biogas Production
        "biogas_production",           # Document
        "biogas_batch",                # Document
        "biogas_quality_check",        # Document
        "biogas_storage_entry",        # Document
        "biogas_consumption",          # Document
        "digestate_production",        # Document
        "digestate_application",       # Document
    ]

    paths = []
    for d in doctype_dirs:
        p = os.path.join(base, d, f"{d}.json")
        if os.path.exists(p):
            paths.append(p)
        else:
            print(f"  ⚠ JSON not found: {p}")
    return paths


def check_doctype_exists(name):
    return frappe.db.exists("DocType", name)


def fix():
    """Create all missing Biogas Management DocTypes."""
    print("=" * 60)
    print("Checking for missing Biogas Management DocTypes...")
    print("=" * 60)

    paths = get_biogas_doctype_paths()
    created = 0
    existed = 0
    failed = 0

    for path in paths:
        with open(path) as f:
            data = json.load(f)

        name = data.get("name", "?")
        module = data.get("module", "?")

        if check_doctype_exists(name):
            print(f"  ✅ {name} — already exists")
            existed += 1
            continue

        print(f"  🔄 {name} — creating (module: {module})...", end=" ")
        try:
            doc = frappe.get_doc(data)
            doc.flags.ignore_links = True
            doc.flags.ignore_permissions = True
            doc.insert()
            frappe.db.commit()
            print("✅")
            created += 1
        except Exception as e:
            frappe.db.rollback()
            print(f"❌ {e}")
            failed += 1

    print()
    print("=" * 60)
    print(f"  Total:    {existed + created + failed}")
    print(f"  Existed:  {existed}")
    print(f"  Created:  {created}")
    print(f"  Failed:   {failed}")
    print("=" * 60)
    print()
    if failed == 0:
        print("✅ All Biogas Management DocTypes are now in the database!")
    else:
        print(f"⚠ {failed} DocType(s) failed. Check errors above.")

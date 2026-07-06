import frappe


def after_install():
	"""Post-install setup: create roles, activate domain, link module."""
	create_roles()
	activate_agriculture_domain()
	link_module_to_domain()


def after_migrate():
	"""Re-apply customizations on every bench migrate: ensure roles, domain, and module linkage."""
	create_roles()
	activate_agriculture_domain()
	link_module_to_domain()


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

import frappe


def after_install():
	"""Post-install setup: create roles, activate domain."""
	create_roles()
	activate_agriculture_domain()


def after_migrate():
	"""Re-apply customizations on every bench migrate: ensure roles exist and domain is active."""
	create_roles()
	activate_agriculture_domain()


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

import frappe
from frappe.model.document import Document


class BiogasProductionSettings(Document):
	def validate(self):
		self.set_setting_name()

	def set_setting_name(self):
		if not self.setting_name:
			self.setting_name = "Biogas Production Settings"

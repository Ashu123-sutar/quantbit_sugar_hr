# Copyright (c) 2026, Quantbit Technologies and contributors
# For license information, please see license.txt

# import frappe
import frappe
from frappe.model.document import Document


class OvertimeEntryLock(Document):
	def before_save(self):
		self.update_ot_lock()
     
	def update_ot_lock(self):
		if self.from_date and self.to_date:
			ot_forms = frappe.get_all(
				"Overtime Entry",
				filters={"date": ["between", [self.from_date, self.to_date]]},
				fields=["name", "ot_lock"]
			)
			for ot in ot_forms:
				frappe.db.set_value("Overtime Entry", ot.name, "ot_lock", 1 if self.lock_ot_form else 0)

# Copyright (c) 2026, Quantbit Technologies and contributors
# For license information, please see license.txt


import frappe
from frappe.model.document import Document
from frappe.utils import getdate

class OvertimeEntry(Document):

	def before_save(self):
		self.set_lock()
		self.check_duplicate_entries()#doubt
		self.check_repeat()
	
	@frappe.whitelist()
	def set_lock(self):
		if self.ot_lock :
			frappe.throw("This Overtime Entry Form is locked and cannot be edited.")

	@frappe.whitelist()
	def is_date_locked(self):
		locked = frappe.get_all("Overtime Entry Lock",filters={"lock_ot_form": 1,"from_date": ["<=", self.date],"to_date": [">=", self.date]},limit=1)
		
		return bool(locked)
   
	def check_repeat(self):
		seen = set()
		for row in self.get("overtime_details"):
			key = (row.employee_id, row.date)
			if key in seen:
				frappe.throw(
					f"कर्मचारी {row.employee_id} यांची {row.date} या तारखेसाठी नोंद आधीच आहे."
				)
			seen.add(key)

	def check_duplicate_entries(self):
		for entry in self.get("overtime_details"):
			duplicate_docs = frappe.db.exists(
				"Overtime Entry Details",
				{
					"employee_id": entry.employee_id,
					"date": entry.date,
					"parent": ["!=", self.name]
				}
			)
			if duplicate_docs:
				frappe.throw(
					f"कर्मचारी {entry.employee_name} ({entry.employee_id}) यांची दिनांक {entry.date} साठी नोंद आधीच झालेली आहे. (ओळ क्रमांक {entry.idx})"
				)
			if (
				getdate(self.date).month != getdate(entry.date).month
				or getdate(self.date).year != getdate(entry.date).year
			):
				frappe.throw(
					f"ओळ क्रमांक {entry.idx}: दिनांक {entry.date} हा फॉर्मच्या तारखेच्या ({self.date}) त्याच महिन्यात असणे आवश्यक आहे."
				)

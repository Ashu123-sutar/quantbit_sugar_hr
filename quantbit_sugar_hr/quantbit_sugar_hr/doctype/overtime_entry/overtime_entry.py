import frappe
from frappe.model.document import Document

class OvertimeEntry(Document):
    def validate(self):
        pairs = set()
        for row in self.overtime_details:
            if not row.employee_id or not row.date:
                continue
            if not row.overtime_hrs or row.overtime_hrs <= 0:
                frappe.throw(f"ओळ क्रमांक {row.idx}: ओव्हरटाईम तास योग्य भरलेले नाहीत.")
            if row.overtime_hrs > 16:
                frappe.throw(
                    f"ओळ क्रमांक {row.idx}: ओव्हरटाईम तास 16 पेक्षा जास्त असू शकत नाहीत."
                )
            key = (row.employee_id, row.date)
            if key in pairs:
                frappe.throw(f"कर्मचारी {row.employee_name} ({row.employee_id}) "f"यांची {row.date} साठी नोंद आधीच आहे (ओळ {row.idx})")
            pairs.add(key)
            self.check_duplicate_in_db(row)
        if self.is_date_locked():
            frappe.throw("हा कालावधी लॉक आहे. एचआर(HR) मॅनेजरशी संपर्क साधा")

    def check_duplicate_in_db(self, row):
        duplicate = frappe.db.sql("""
            SELECT ted.parent
            FROM `tabOvertime Entry Details` ted
            INNER JOIN `tabOvertime Entry` te
                ON te.name = ted.parent
            WHERE
                ted.employee_id = %s
                AND ted.date = %s
                AND ted.parent != %s
                AND te.docstatus != 2
            LIMIT 1
        """, (
            row.employee_id,
            row.date,
            self.name or ""
        ), as_dict=True)
        if duplicate:
            form_name = duplicate[0].parent
            frappe.throw(
                f"कर्मचारी {row.employee_name} ({row.employee_id}) "f"यांची {row.date} साठी नोंद आधीच फॉर्म {form_name} मध्ये आहे "f"(ओळ {row.idx})"
            )

    @frappe.whitelist()
    def is_date_locked(self):
        if not self.date:
            return False
        return frappe.db.exists(
            "Overtime Entry Lock",
            {
                "lock_ot_form": 1,"from_date": ["<=", self.date],"to_date": [">=", self.date]
            }
        )

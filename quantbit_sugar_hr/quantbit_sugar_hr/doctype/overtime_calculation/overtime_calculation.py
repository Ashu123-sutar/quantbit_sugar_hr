# Copyright (c) 2026, Quantbit Technologies and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import getdate
from frappe import _

class OvertimeCalculation(Document):

    @frappe.whitelist()
    def get_overtime(self):
        self.set("overtime_details", [])
        self.set("overtime_hours_calculation", [])
        num_days = 0
        try:
            num_days = (getdate(self.to_date) - getdate(self.from_date)).days + 1
            from_date = getdate(self.from_date)
        except Exception as e:
            frappe.throw(_("Invalid 'From Date'. Error: {0}").format(e))
            return
        overtime_ids = [
            d.overtime_id
            for d in self.get("supevisor_details")
            if d.check
        ]
        if not overtime_ids:
            frappe.msgprint("कृपया किमान एक ओव्हरटाईम नोंद निवडा.")
            return
        data = frappe.db.sql("""
            SELECT
                oe.name AS overtime_id,
                oe.date,
                oe.supervisor,
                oe.supervisor_name,
                oed.employee_id,
                oed.employee_name,
                oed.overtime_hrs,
                epd.from_date AS payroll_from_date,
                epd.basic,
                epd.hra,
                epd.lta,
                epd.ca,
                epd.medical_allowance,
                epd.fda,
                epd.bonus,
                epd.da,
                epd.overtime_ot,
                epd.leave_encashment,
                epd.washing_allowance
            FROM `tabOvertime Entry` oe
            INNER JOIN `tabOvertime Entry Details` oed
                ON oe.name = oed.parent
            LEFT JOIN `tabEmployee Payroll Details` epd
                ON epd.parent = oed.employee_id
            WHERE oe.name IN %(overtime_ids)s
        """, {
            "overtime_ids": tuple(overtime_ids)
        }, as_dict=True)
        if not data:
            frappe.msgprint("कोणतीही ओव्हरटाईम माहिती आढळली नाही.")
            return
        latest_payroll = {}
        for row in data:
            key = (row.employee_id, row.overtime_id)
            if key in latest_payroll:
                continue
            if row.payroll_from_date and from_date < row.payroll_from_date:
                continue
            latest_payroll[key] = row
        for row in latest_payroll.values():
            total_amt = (
                (row.basic or 0) +
                (row.hra or 0) +
                (row.lta or 0) +
                (row.ca or 0) +
                (row.medical_allowance or 0) +
                (row.fda or 0) +
                (row.bonus or 0) +
                (row.da or 0) +
                (row.overtime_ot or 0) +
                (row.leave_encashment or 0) +
                (row.washing_allowance or 0)
            )
            if num_days > 0:
                daily = total_amt / num_days
                rate = daily / 8
            else:
                rate = 0
            self.append("overtime_details", {
                "overtime_id": row.overtime_id,
                "supervisor_name": row.supervisor_name,
                "supervisor_id": row.supervisor,
                "employee_name": row.employee_name,
                "employee_id": row.employee_id,
                "date": row.date,
                "overtime_hrs": row.overtime_hrs,
                "overtime_rate": rate,
                "total_amount": rate * row.overtime_hrs
            })
        self.get_employee_sum()


    def get_employee_sum(self):
        employee_id_dict = {}     
        for i in self.get("overtime_details"):
            if i.employee_id not in employee_id_dict:
                employee_id_dict[i.employee_id] = {
                    "employee_name": i.employee_name,
                    "employee_id": i.employee_id,
                    "overtime_rate": i.overtime_rate,
                    "overtime_hrs": i.overtime_hrs,
                    "total_amount": i.total_amount
                }
            else:
                employee_id_dict[i.employee_id]['total_amount'] += i.total_amount
                employee_id_dict[i.employee_id]['overtime_hrs'] += i.overtime_hrs

        for data in employee_id_dict.values():
            self.append("overtime_hours_calculation", {
                "employee_name": data['employee_name'],
                "employee_id": data['employee_id'],
                "overtime_rate": data['overtime_rate'],
                "overtime_hrs": data['overtime_hrs'],
                "total_overtime_amount": data['total_amount'],
                "start_date": self.from_date,
                "end_date": self.to_date
            })


// Copyright (c) 2026, Quantbit Technologies and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Overtime Entry Lock", {
// 	refresh(frm) {

// 	},
// });
frappe.ui.form.on("Overtime Entry Lock", {
    from_date: function(frm) {
        if (frm.doc.from_date) {
            let d = new Date(frm.doc.from_date);

            // Set form_date to 1st of month
            frm.set_value('from_date', frappe.datetime.obj_to_str(new Date(d.getFullYear(), d.getMonth(), 1)));

            // Set to_date to last day of month
            frm.set_value('to_date', frappe.datetime.obj_to_str(new Date(d.getFullYear(), d.getMonth() + 1, 0)));
        }
    }
});
// Copyright (c) 2025, Quantbit Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

frappe.ui.form.on("Overtime Entry", {
    refresh: function(frm) {
                     $('.layout-side-section').hide();
                     $('.layout-main-section-wrapper').css('margin-left', '0');
    }
});

frappe.ui.form.on("Overtime Entry", {
    refresh(frm) {
        check_ot_lock(frm);
    },
    date(frm) {
        check_ot_lock(frm);
    }
});

function check_ot_lock(frm) {
    if (!frm.doc.date) return;
    frappe.call({
        method: "is_date_locked",
        doc: frm.doc,
        callback(r) {
            if (r.message) {
                frm.set_value("ot_lock", 1);
                frappe.msgprint("हा कालावधी लॉक आहे. ओव्हरटाईम नोंद करता येणार नाही.");
            } else {
                frm.set_value("ot_lock", 0);
            }
            frm.refresh_field("ot_lock");
        }
    });
}

frappe.ui.form.on("Overtime Entry Details", {
    overtime_details_add(frm, cdt, cdn) {
        let row = locals[cdt][cdn];
        if (!row.date && frm.doc.date) {
            row.date = frm.doc.date;
        }
    }
});

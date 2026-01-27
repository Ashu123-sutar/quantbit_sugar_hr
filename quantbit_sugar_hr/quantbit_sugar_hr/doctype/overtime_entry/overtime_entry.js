// Copyright (c) 2026, Quantbit Technologies and contributors
// For license information, please see license.txt

frappe.ui.form.on("Overtime Entry", {
    refresh: function(frm) {
                     $('.layout-side-section').hide();
                     $('.layout-main-section-wrapper').css('margin-left', '0');
    }
});

frappe.ui.form.on('Overtime Entry', {
    date: function(frm) {
        if (!frm.doc.date) 
            return;

        frappe.call({
            method: "is_date_locked",
            doc:frm.doc,
            callback: function(r) {
                if (r.message === true) {
                    frappe.msgprint("The selected date is locked for OT. You cannot make changes.");
                    frm.set_value("ot_lock", 1);  
                    frm.refresh_field("ot_lock");
                } else {
                    frm.set_value("ot_lock", 0);  
                    frm.refresh_field("ot_lock");
                }
            }
        });
    }
});




frappe.ui.form.on("Supplier", {
    refresh(frm) {
        // if (!frm.is_new()) {
            frm.add_custom_button(__('Create Employee'), () => {
                if (!frm.doc.custom_first_name) {
                    frappe.msgprint(__('Please select the First Name'));
                    return;
                }
                if (!frm.doc.custom_gender) {
                    frappe.msgprint(__('Please select the Gender'));
                    return;
                }
                if (!frm.doc.custom_date_of_birth) {
                    frappe.msgprint(__('Please select the Date Of Birth'));
                    return;
                }
                if (frm.doc.custom_aadhaar_number === 0) {
                    frappe.msgprint(__('Please add the Aadhaar Number'));
                    return;
                }
                let d = new frappe.ui.Dialog({
                    title: __('Create Employee'),
                    fields: [
                        {
                            fieldname: 'date_of_joinning',
                            label: 'Date of Joining',
                            fieldtype: 'Date',
                            reqd: 1
                        },
                    ],
                    primary_action_label: __('Create'),
                    primary_action(values) {
                        frappe.call({
                            method: 'quantbit_hr_plus.hr_plus.attendance_override.create_employee',
                            args: {
                                docname: frm.doc.name,
                                date_of_joining: values.date_of_joinning
                            },
                            callback: function (r) {
                                if (r.message) {
                                    frappe.msgprint(__('Employee Created Successfully: {0}', [r.message]));
                                    console.log(r.message);
                                }
                                d.hide();
                            }
                        });
                    }
                });

                d.show();

            }, __("Create"));
        }
    // },

});
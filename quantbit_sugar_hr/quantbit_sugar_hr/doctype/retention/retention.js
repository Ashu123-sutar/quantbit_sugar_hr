// Copyright (c) 2025, Quantbit Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

frappe.ui.form.on('Retention', {
	from_date: function(frm) {
		frm.call({
			method:"check_dates",
			doc:frm.doc
		})
	},
	to_date: function(frm) {
		frm.call({
			method:"check_dates",
			doc:frm.doc
		})
	},
});
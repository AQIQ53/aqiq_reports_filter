// Copyright (c) 2016, AQIQ and contributors
// For license information, please see license.txt

frappe.ui.form.on('Aqiq Report Filter', {
    refresh: function(frm) {
		frm.events.setup_fieldname_select(frm);
	},
	report_doctype: function(frm) {
		frm.events.setup_fieldname_select(frm);
	},
    setup_fieldname_select: function(frm) {
		// get the doctype to update fields
		if (!frm.doc.report_doctype) {
			return;
		}

		frappe.model.with_doctype(frm.doc.report_doctype, function() {
			let get_select_options = function(df, parent_field) {
                if (df.fieldtype == "Link" || df.fieldtype == "Table"){
                    // Append parent_field name along with fieldname for child table fields
                    let select_value = parent_field ? df.fieldname + ',' + parent_field : df.fieldname;

                    return {
                        value: select_value,
                        label: df.fieldname + ' (' + __(df.label) + ')'
                    };
                }
				
			};


			let fields = frappe.get_doc('DocType', frm.doc.report_doctype).fields;
			let options = $.map(fields, function(d) {
				return in_list(frappe.model.no_value_type, d.fieldtype)
					? null : get_select_options(d);
			});

			// set value changed options
			frm.set_df_property(
				'fieldname',
				'options',
				[''].concat(options)
			);

		});
	},
});


import datetime
from copy import deepcopy
import frappe
from frappe.core.doctype.report.report import Report
from frappe import _, scrub

def get_report_module_dotted_path(module, report_name):
	return frappe.local.module_app[scrub(module)] + "." + scrub(module) \
		+ ".report." + scrub(report_name) + "." + scrub(report_name)

def execute_module(self, filters):
	# report in python module
	module = self.module or frappe.db.get_value("DocType", self.ref_doctype, "module")
	method_name = get_report_module_dotted_path(module, self.name) + ".execute"
	results = frappe.get_attr(method_name)(frappe._dict(filters))
	return get_filtered_results(results, module)
	

def get_filtered_results(results, module):
	if frappe.session.user != "Administrator" and results and results[1] and len(results[1]) > 0:
		doctypes = frappe.db.get_all("Aqiq Report Filter", {"report_module": module}, "*")

		if not doctypes or not doctypes[0]: return results

		for doctype_op in results[0]:

			if not doctype_op.get("options"): continue

			for doctype in doctypes:
				if doctype_op.get("options") == doctype.report_doctype:
					results = apply_user_permissions(results, doctype.report_doctype, doctype.fieldname, doctype_op.get("fieldname"))
					frappe.msgprint("Test: " + str(len(results[1])))
	return results

def apply_user_permissions(results, doctype, fieldname, report_field):
	results = list(results)
	temp_res = deepcopy(results)

	field_doctype = frappe.get_meta(doctype).get_link_doctype(fieldname)
	permissions = frappe.db.get_list("User Permission",filters={'user': frappe.session.user,'allow': field_doctype}, fields=["for_value"])
	if permissions and permissions[0]:
		temp_res[1] = []
		permissions = [p['for_value'] for p in permissions]
		for row in results[1]:
			if frappe.db.get_value(doctype, row.get(report_field), fieldname) in permissions:
				temp_res[1].append(row)
	temp_res = tuple(temp_res)
	
	return temp_res

Report.execute_module = execute_module
import frappe, json

from frappe.utils import flt, cint

def rate_to_decimal(rate):
	"""Converts from percentage format to decimal"""
	return flt(rate) / flt(100.000)

@frappe.whitelist()
def create_loan_from_appl(doc):
	"""Creates a Loan taking a Loan Application as a base
	:param doc: is the Loan Application object"""
	from frappe.model.mapper import get_mapped_doc

	if isinstance(doc, basestring):
		doc = frappe._dict(json.loads(doc))

	def post_process(source_doc, target_doc):
		target_doc.set_missing_values()

	target_doc = frappe.new_doc("Loan")

	return get_mapped_doc(doc.doctype, doc.name, {
		"Loan Application": {
			"doctype": "Loan",
			"field_map": {
				"name": "loan_application",
				"approved_net_amount": "loan_amount"
			}
		}
	}, target_doc, post_process)

@frappe.whitelist()
def create_loan_appl_from_tool(doc):
	"""Creates a Loan Application  taking an Amortization Tool
	:param doc: is the Amortization Tool object"""
	from frappe.model.mapper import get_mapped_doc

	if isinstance(doc, basestring):
		doc = frappe._dict(json.loads(doc))

	def post_process(source_doc, target_doc):
		target_doc.set_missing_values()

	target_doc = frappe.new_doc("Loan Application")

	return get_mapped_doc(doc.doctype, doc.name, {
		"Amortization Tool": {
			"doctype": "Loan Application"
		}
	}, target_doc, post_process)

@frappe.whitelist()
def get_loan(doctype, docname):
	"""Returns an existing Loan from the DB and adds the income_account_currency
	into the __onload property

	:param doctype: should be Loan
	:param docname: should be Loan Name"""
	
	doc = frappe.get_doc(doctype, docname)

	income_account_currency = frappe.get_value("Account", 
		doc.income_account, "account_currency")

	doc.set_onload("income_account_currency", income_account_currency)

	return doc.as_dict()

@frappe.whitelist()
def create_insurance_card_from_loan(doc):
	from frappe.model.mapper import get_mapped_doc

	if isinstance(doc, basestring):
		doc = frappe._dict(json.loads(doc))

	def post_process(source_doc, target_doc):
		target_doc.set_default_values()

	target_doc = frappe.new_doc("Insurance Card")

	return get_mapped_doc(doc.doctype, doc.name, {
		"Loan": {
			"doctype": "Insurance Card"
		}
	}, target_doc, post_process)
	
@frappe.whitelist()
def add_rows_to_income_receipt_table(doc, selections, args):
	if isinstance(doc, basestring):
		doc = frappe.get_doc(json.loads(doc))

	doc.grab_loan_charges(False, selections)

	return doc.as_dict()


import frappe

def before_install():
	"""runs before installation"""
	add_reqd_roles()

def after_install():
	"""runs after installation"""
	# update_customer_icons()
	pass

def add_reqd_roles():
	"""adds default roles for the app to run"""

	from fimax.hook.role import create_simple_role
	role_list = ["Loan Approver", "Loan Manager", "Loan User", "CEO", 
		"Cashier", "General Manager", "Finance Manager", "Finance User",
		"Collector User", "Collector Manager"]

	for role in role_list:
		if frappe.db.exists("Role", role): 
			continue

		doc = create_simple_role(role)
		doc.save()

	# save the changes to the database
	frappe.db.commit()

def update_customer_icons():
	"""removes default apps' icon from desktop"""

	customer_icons = frappe.get_list("Desktop Icon", {
		"module_name": "Customer",
	}, ["name"])

	update_them(customer_icons)

def update_them(icon_list):
	"""hide a list of icons"""
	
	doctype = "Desktop Icon"

	for icon in icon_list:
		doc = frappe.get_doc(doctype, icon)
		doc.update({
			"color": "#469",
			"icon": "fa fa-user-circle-o",
			"type": "link",
			"link": "List/Customer/List"
		})

		doc.db_update()
	
	# save the changes to the database
	frappe.db.commit()

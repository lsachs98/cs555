def getName(e):
	return e.get_name()

def order_children_by_age(families):
	ordered_children = []
	
	for family in families:
		to_order = family.get_children()
		to_order.sort(key = getName)
		ordered_children.append(to_order)

	return ordered_children

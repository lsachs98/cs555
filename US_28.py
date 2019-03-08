def getName(e):
	return e.get_name()

def order_children_by_age(families):
	ordered_children = []
	
	for family in families:
		these_children = []
		to_order = family.get_children()
		to_order.sort(key = getName)

		for child in to_order:
			these_children.append(child.get_id())

		ordered_children.append(these_children)

	return ordered_children

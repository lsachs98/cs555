#user story 29, list all deceased
def list_deceased(GEDinfo):
	all_individuals = GEDinfo.individuals()
	deceased = []
	for i in all_individuals:
		if i.get_death() != "NA":
			deceased.append(i)

	return deceased
	
